from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

import requests

from prolog_bridge import list_players
from visual_data import (
    PLAYER_IMAGE_URL,
    PLAYERS_ASSETS_DIR,
    TEAM_METADATA,
    TEAMS_ASSETS_DIR,
    TRANSFERMARKT_DATA_PATH,
    player_image_path,
    slugify,
)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}
SEARCH_URL = "https://www.transfermarkt.com/schnellsuche/ergebnis/schnellsuche"


def _name_key(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", "", normalized.lower())


def _download_requests(url: str, destination: Path) -> bool:
    try:
        response = requests.get(url, headers=HEADERS, timeout=8)
        content_type = response.headers.get("Content-Type", "")
        if response.status_code != 200 or not content_type.startswith("image/"):
            return False
        destination.write_bytes(response.content)
        return True
    except requests.RequestException:
        return False


def _token_key(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii").lower())


def _search_transfermarkt_photo(player_name: str) -> str | None:
    query = unicodedata.normalize("NFKD", player_name).encode("ascii", "ignore").decode("ascii")
    try:
        response = requests.get(SEARCH_URL, params={"query": query}, headers=HEADERS, timeout=12)
        if response.status_code != 200:
            return None
        html = response.text
    except requests.RequestException:
        return None

    # Candidate profile links from search results.
    links = re.findall(r'href="(/[^"]*/profil/spieler/\d+)"', html)
    if not links:
        return None

    query_key = _token_key(player_name)
    best_profile = None
    best_score = -1
    seen: set[str] = set()
    for rel in links[:30]:
        if rel in seen:
            continue
        seen.add(rel)
        slug = rel.split("/profil/spieler/")[0].strip("/").split("/")[-1]
        score = 0
        slug_key = _token_key(slug.replace("-", " "))
        if slug_key == query_key:
            score += 100
        if query_key in slug_key or slug_key in query_key:
            score += 50
        # token overlap
        q_tokens = set(re.findall(r"[a-z0-9]+", query.lower()))
        s_tokens = set(re.findall(r"[a-z0-9]+", slug.lower().replace("-", " ")))
        score += len(q_tokens & s_tokens) * 10
        if score > best_score:
            best_score = score
            best_profile = rel

    if not best_profile:
        return None

    profile_url = f"https://www.transfermarkt.com{best_profile}"
    try:
        page = requests.get(profile_url, headers=HEADERS, timeout=12)
        if page.status_code != 200:
            return None
        profile_html = page.text
    except requests.RequestException:
        return None

    image_match = re.search(
        r'https://img\.a\.transfermarkt\.technology/portrait/(?:header|medium)/[^"\']+',
        profile_html,
    )
    if not image_match:
        return None
    return image_match.group(0)


def _transfermarkt_team_squad(team_name: str, team_url: str) -> list[dict]:
    try:
        response = requests.get(team_url, headers=HEADERS, timeout=10)
        if response.status_code != 200:
            return []
        html = response.text
    except requests.RequestException:
        return []

    result: list[dict] = []
    seen_ids: set[str] = set()

    # Parse row by row to avoid cross-row mismatches name <-> image.
    rows = re.findall(r"<tr[^>]*>(.*?)</tr>", html, flags=re.DOTALL | re.IGNORECASE)
    for row in rows:
        image_match = re.search(
            r'data-src="(https://img\.a\.transfermarkt\.technology/portrait/medium/[^"]+)"',
            row,
            flags=re.IGNORECASE,
        )
        player_match = re.search(
            r'<a href="(/[^"]*/profil/spieler/(\d+))">\s*([^<]+)\s*</a>',
            row,
            flags=re.DOTALL | re.IGNORECASE,
        )
        if not image_match or not player_match:
            continue

        image_url = image_match.group(1).strip()
        profile_path = player_match.group(1).strip()
        player_id = player_match.group(2).strip()
        display_name = player_match.group(3).strip()
        if not display_name or player_id in seen_ids:
            continue
        seen_ids.add(player_id)

        result.append(
            {
                "team": team_name,
                "player_id": player_id,
                "name": display_name,
                "name_key": _name_key(display_name),
                "profile_url": f"https://www.transfermarkt.com{profile_path}",
                "image_url": image_url,
                "local_image": "",
            }
        )
    return result


def main() -> None:
    PLAYERS_ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    TEAMS_ASSETS_DIR.mkdir(parents=True, exist_ok=True)

    players = list_players()
    players_by_key = {_name_key(player): player for player in players}
    tm_downloaded = 0
    tm_failed = 0
    static_downloaded = 0
    static_failed = 0
    player_search_downloaded = 0
    player_search_failed = 0
    logos_downloaded = 0
    logos_failed = 0
    generated_avatars = 0
    squads_output: dict[str, list[dict]] = {}

    # Hard reset stale photos from previous buggy mappings.
    for stale in PLAYERS_ASSETS_DIR.glob("tm-*.jpg"):
        stale.unlink(missing_ok=True)
    for player in players:
        alias_path = PLAYERS_ASSETS_DIR / f"{slugify(player)}.jpg"
        if alias_path.exists():
            alias_path.unlink(missing_ok=True)

    # 1) Download team logos from Transfermarkt CDN.
    for team_name, meta in TEAM_METADATA.items():
        club_id = meta.get("club_id")
        if club_id is None:
            continue
        logo_url = f"https://tmssl.akamaized.net/images/wappen/head/{club_id}.png"
        logo_path = TEAMS_ASSETS_DIR / f"{slugify(team_name)}.png"
        if logo_path.exists():
            continue
        if _download_requests(logo_url, logo_path):
            logos_downloaded += 1
        else:
            logos_failed += 1

    # 2) Scrape each team squad and download player portraits locally.
    for team_name, meta in TEAM_METADATA.items():
        team_url = meta.get("transfermarkt_url")
        if not team_url:
            squads_output[team_name] = []
            continue
        squad = _transfermarkt_team_squad(team_name, team_url)
        for item in squad:
            tm_path = PLAYERS_ASSETS_DIR / f"tm-{item['player_id']}.jpg"
            if not tm_path.exists():
                ok = _download_requests(item["image_url"], tm_path)
                if ok:
                    tm_downloaded += 1
                else:
                    tm_failed += 1
            item["local_image"] = str(tm_path if tm_path.exists() else "")

            # If this player exists in Prolog by name, also create alias image for app matching.
            maybe_prolog_name = players_by_key.get(item["name_key"])
            if maybe_prolog_name:
                alias_path = PLAYERS_ASSETS_DIR / f"{slugify(maybe_prolog_name)}.jpg"
                if tm_path.exists():
                    alias_path.write_bytes(tm_path.read_bytes())
        squads_output[team_name] = squad

    # 3) Fallback static images for known players.
    for player, url in PLAYER_IMAGE_URL.items():
        path = PLAYERS_ASSETS_DIR / f"{slugify(player)}.jpg"
        # Replace any previous alias to avoid stale/wrong mappings.
        if path.exists():
            path.unlink(missing_ok=True)
        ok = _download_requests(url, path)
        if ok:
            static_downloaded += 1
        else:
            static_failed += 1

    # 4) Ensure every Prolog player has at least local avatar SVG.
    for player in players:
        player_jpg = PLAYERS_ASSETS_DIR / f"{slugify(player)}.jpg"
        if not player_jpg.exists():
            candidate = _search_transfermarkt_photo(player)
            if candidate and _download_requests(candidate, player_jpg):
                player_search_downloaded += 1
            else:
                player_search_failed += 1
        image_path = Path(player_image_path(player, use_real_when_available=True))
        if image_path.suffix == ".svg":
            generated_avatars += 1

    TRANSFERMARKT_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    TRANSFERMARKT_DATA_PATH.write_text(
        json.dumps(squads_output, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("Assets preparados:")
    print(f"- Logos de equipos descargados: {logos_downloaded}")
    print(f"- Logos fallidos: {logos_failed}")
    print(f"- Transfermarkt descargadas: {tm_downloaded}")
    print(f"- Transfermarkt fallidas: {tm_failed}")
    print(f"- Fotos estáticas descargadas: {static_downloaded}")
    print(f"- Fotos estáticas fallidas: {static_failed}")
    print(f"- Fotos por búsqueda de jugador: {player_search_downloaded}")
    print(f"- Búsquedas sin foto: {player_search_failed}")
    print(f"- Jugadores con avatar local: {generated_avatars}")
    print(f"- Carpeta: {PLAYERS_ASSETS_DIR}")
    print(f"- Dataset squads: {TRANSFERMARKT_DATA_PATH}")


if __name__ == "__main__":
    main()
