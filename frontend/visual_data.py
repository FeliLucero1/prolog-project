from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from functools import lru_cache
from pathlib import Path


TEAM_METADATA = {
    "Real Madrid": {
        "logo_url": "https://upload.wikimedia.org/wikipedia/en/5/56/Real_Madrid_CF.svg",
        "color": "#FEBE10",
        "rivals": {"Barcelona", "PSG"},
        "description": "Club con enfoque en talento joven + figuras consolidadas.",
        "transfermarkt_url": "https://www.transfermarkt.com/real-madrid/startseite/verein/418",
        "club_id": 418,
    },
    "Barcelona": {
        "logo_url": "https://upload.wikimedia.org/wikipedia/en/4/47/FC_Barcelona_%28crest%29.svg",
        "color": "#A50044",
        "rivals": {"Real Madrid", "Liverpool"},
        "description": "Proyecto tecnico con peso en cantera y posesion.",
        "transfermarkt_url": "https://www.transfermarkt.com/fc-barcelona/startseite/verein/131",
        "club_id": 131,
    },
    "Manchester City": {
        "logo_url": "https://upload.wikimedia.org/wikipedia/en/e/eb/Manchester_City_FC_badge.svg",
        "color": "#6CABDD",
        "rivals": {"Liverpool", "PSG"},
        "description": "Plantilla amplia, alto presupuesto y control del juego.",
        "transfermarkt_url": "https://www.transfermarkt.com/manchester-city/startseite/verein/281",
        "club_id": 281,
    },
    "Bayern Munich": {
        "logo_url": "https://upload.wikimedia.org/wikipedia/commons/1/1f/FC_Bayern_M%C3%BCnchen_logo_%282017%29.svg",
        "color": "#DC052D",
        "rivals": {"PSG", "Barcelona"},
        "description": "Estructura competitiva con equilibrio tactico y fisico.",
        "transfermarkt_url": "https://www.transfermarkt.com/fc-bayern-munich/startseite/verein/27",
        "club_id": 27,
    },
    "PSG": {
        "logo_url": "https://upload.wikimedia.org/wikipedia/en/a/a7/Paris_Saint-Germain_F.C..svg",
        "color": "#004170",
        "rivals": {"Real Madrid", "Bayern Munich", "Manchester City"},
        "description": "Club orientado a rendimiento inmediato y figuras top.",
        "transfermarkt_url": "https://www.transfermarkt.com/paris-saint-germain/startseite/verein/583",
        "club_id": 583,
    },
    "Liverpool": {
        "logo_url": "https://upload.wikimedia.org/wikipedia/en/0/0c/Liverpool_FC.svg",
        "color": "#C8102E",
        "rivals": {"Manchester City", "Barcelona"},
        "description": "Intensidad alta, transiciones rapidas y pressing.",
        "transfermarkt_url": "https://www.transfermarkt.com/liverpool-fc/startseite/verein/31",
        "club_id": 31,
    },
    "Arsenal": {
        "logo_url": "",
        "color": "#EF0107",
        "rivals": set(),
        "description": "Equipo competitivo de la Premier con estructura joven.",
        "transfermarkt_url": "https://www.transfermarkt.com/fc-arsenal/startseite/verein/11",
        "club_id": 11,
    },
    "Inter": {
        "logo_url": "",
        "color": "#0068A8",
        "rivals": set(),
        "description": "Potencia italiana con plantel equilibrado.",
        "transfermarkt_url": "https://www.transfermarkt.com/inter-mailand/startseite/verein/46",
        "club_id": 46,
    },
    "Atletico Madrid": {
        "logo_url": "",
        "color": "#CB3524",
        "rivals": set(),
        "description": "Bloque defensivo fuerte y juego intenso.",
        "transfermarkt_url": "https://www.transfermarkt.com/atletico-madrid/startseite/verein/13",
        "club_id": 13,
    },
    "Chelsea": {
        "logo_url": "",
        "color": "#034694",
        "rivals": set(),
        "description": "Plantilla amplia con talento joven.",
        "transfermarkt_url": "https://www.transfermarkt.com/fc-chelsea/startseite/verein/631",
        "club_id": 631,
    },
    "Juventus": {
        "logo_url": "",
        "color": "#111111",
        "rivals": set(),
        "description": "Histórico de Serie A con experiencia europea.",
        "transfermarkt_url": "https://www.transfermarkt.com/juventus-turin/startseite/verein/506",
        "club_id": 506,
    },
    "Manchester United": {
        "logo_url": "",
        "color": "#DA291C",
        "rivals": set(),
        "description": "Club histórico de la Premier League.",
        "transfermarkt_url": "https://www.transfermarkt.com/manchester-united/startseite/verein/985",
        "club_id": 985,
    },
    "AC Milan": {
        "logo_url": "",
        "color": "#A00014",
        "rivals": set(),
        "description": "Tradición europea y escuela táctica italiana.",
        "transfermarkt_url": "https://www.transfermarkt.com/ac-mailand/startseite/verein/5",
        "club_id": 5,
    },
    "Borussia Dortmund": {
        "logo_url": "",
        "color": "#FDE100",
        "rivals": set(),
        "description": "Identidad ofensiva y desarrollo de talento.",
        "transfermarkt_url": "https://www.transfermarkt.com/borussia-dortmund/startseite/verein/16",
        "club_id": 16,
    },
    "Bayer Leverkusen": {
        "logo_url": "",
        "color": "#D00027",
        "rivals": set(),
        "description": "Proyecto moderno de alta intensidad.",
        "transfermarkt_url": "https://www.transfermarkt.com/bayer-04-leverkusen/startseite/verein/15",
        "club_id": 15,
    },
    "Tottenham": {
        "logo_url": "",
        "color": "#132257",
        "rivals": set(),
        "description": "Equipo top de Inglaterra con ritmo alto.",
        "transfermarkt_url": "https://www.transfermarkt.com/tottenham-hotspur/startseite/verein/148",
        "club_id": 148,
    },
    "Napoli": {
        "logo_url": "",
        "color": "#0094D9",
        "rivals": set(),
        "description": "Referencia reciente de Serie A.",
        "transfermarkt_url": "https://www.transfermarkt.com/ssc-neapel/startseite/verein/6195",
        "club_id": 6195,
    },
    "RB Leipzig": {
        "logo_url": "",
        "color": "#E31B23",
        "rivals": set(),
        "description": "Modelo alemán dinámico y vertical.",
        "transfermarkt_url": "https://www.transfermarkt.com/rasenballsport-leipzig/startseite/verein/23826",
        "club_id": 23826,
    },
    "Benfica": {
        "logo_url": "",
        "color": "#E31E24",
        "rivals": set(),
        "description": "Gigante portugués con cantera fuerte.",
        "transfermarkt_url": "https://www.transfermarkt.com/benfica-lissabon/startseite/verein/294",
        "club_id": 294,
    },
    "Porto": {
        "logo_url": "",
        "color": "#004B93",
        "rivals": set(),
        "description": "Club competitivo europeo de Portugal.",
        "transfermarkt_url": "https://www.transfermarkt.com/fc-porto/startseite/verein/720",
        "club_id": 720,
    },
}


PLAYER_CLUB = {
    "Lionel Messi": "Inter Miami",
    "Cristiano Ronaldo": "Al Nassr",
    "Kylian Mbappé": "Real Madrid",
    "Erling Haaland": "Manchester City",
    "Robert Lewandowski": "Barcelona",
    "Karim Benzema": "Al Ittihad",
    "Kevin De Bruyne": "Manchester City",
    "Luka Modrić": "Real Madrid",
    "Bruno Fernandes": "Manchester United",
    "Pedri": "Barcelona",
    "Jude Bellingham": "Real Madrid",
    "Federico Valverde": "Real Madrid",
    "Rodri": "Manchester City",
    "Toni Kroos": "Retirado",
    "Virgil van Dijk": "Liverpool",
    "Rúben Dias": "Manchester City",
    "Marquinhos": "PSG",
    "Alessandro Bastoni": "Inter",
    "Ronald Araújo": "Barcelona",
    "David Alaba": "Real Madrid",
    "Theo Hernández": "AC Milan",
    "Alisson": "Liverpool",
    "Thibaut Courtois": "Real Madrid",
    "Marc-André ter Stegen": "Barcelona",
    "Jan Oblak": "Atletico Madrid",
    "Gianluigi Donnarumma": "PSG",
    "Gavi": "Barcelona",
    "Eduardo Camavinga": "Real Madrid",
    "Jamal Musiala": "Bayern Munich",
    "Bukayo Saka": "Arsenal",
    "Sergio Ramos": "Sevilla",
    "Iker Casillas": "Leyenda",
    "Neymar": "Al Hilal",
    "Frenkie de Jong": "Barcelona",
    "Vinicius Junior": "Real Madrid",
    "Mohamed Salah": "Liverpool",
    "Lautaro Martinez": "Inter",
    "Harry Kane": "Bayern Munich",
    "Antoine Griezmann": "Atletico Madrid",
    "Martin Odegaard": "Arsenal",
    "Declan Rice": "Arsenal",
    "Bernardo Silva": "Manchester City",
    "Florian Wirtz": "Bayer Leverkusen",
    "Enzo Fernandez": "Chelsea",
    "Cole Palmer": "Chelsea",
    "Lamine Yamal": "Barcelona",
    "William Saliba": "Arsenal",
    "Lisandro Martinez": "Manchester United",
    "Antonio Rudiger": "Real Madrid",
    "Pau Cubarsi": "Barcelona",
    "Joao Cancelo": "Al Hilal",
    "Emiliano Martinez": "Aston Villa",
    "Mike Maignan": "AC Milan",
    "Ederson": "Manchester City",
}


# Fotos reales (Wikimedia Commons). Se descargan localmente con prepare_assets.py.
PLAYER_IMAGE_URL = {
    "Lionel Messi": "https://upload.wikimedia.org/wikipedia/commons/b/b4/Lionel-Messi-Argentina-2022-FIFA-World-Cup_%28cropped%29.jpg",
    "Cristiano Ronaldo": "https://upload.wikimedia.org/wikipedia/commons/a/a7/Cristiano_Ronaldo_playing_for_Al_Nassr_FC%2C_September_2023.jpg",
    "Kylian Mbappé": "https://upload.wikimedia.org/wikipedia/commons/0/0c/Kylian_Mbapp%C3%A9_2019.jpg",
    "Erling Haaland": "https://upload.wikimedia.org/wikipedia/commons/9/94/Erling_Haaland_2023.jpg",
    "Robert Lewandowski": "https://upload.wikimedia.org/wikipedia/commons/8/8d/Robert_Lewandowski_2019.jpg",
    "Karim Benzema": "https://upload.wikimedia.org/wikipedia/commons/0/02/Karim_Benzema_2022.jpg",
    "Kevin De Bruyne": "https://upload.wikimedia.org/wikipedia/commons/7/7a/Kevin_De_Bruyne_playing_for_Manchester_City_F.C._%28cropped%29.jpg",
    "Luka Modrić": "https://upload.wikimedia.org/wikipedia/commons/5/5d/Luka_Modri%C4%87_2022.jpg",
    "Bruno Fernandes": "https://upload.wikimedia.org/wikipedia/commons/2/2b/Bruno_Fernandes_2021.jpg",
    "Pedri": "https://upload.wikimedia.org/wikipedia/commons/5/5d/Pedri_2021.jpg",
    "Jude Bellingham": "https://upload.wikimedia.org/wikipedia/commons/8/89/Jude_Bellingham_2023.jpg",
    "Federico Valverde": "https://upload.wikimedia.org/wikipedia/commons/2/2e/Federico_Valverde_2022.jpg",
    "Rodri": "https://upload.wikimedia.org/wikipedia/commons/2/29/Rodri_2023.jpg",
    "Virgil van Dijk": "https://upload.wikimedia.org/wikipedia/commons/4/4f/Virgil_van_Dijk_2018.jpg",
    "Rúben Dias": "https://upload.wikimedia.org/wikipedia/commons/6/6a/R%C3%BAben_Dias_2021.jpg",
    "Marquinhos": "https://upload.wikimedia.org/wikipedia/commons/2/2c/Marquinhos_2018.jpg",
    "Ronald Araújo": "https://upload.wikimedia.org/wikipedia/commons/4/4a/Ronald_Ara%C3%BAjo_2021.jpg",
    "Alisson": "https://upload.wikimedia.org/wikipedia/commons/0/05/Alisson_Becker_2018.jpg",
    "Thibaut Courtois": "https://upload.wikimedia.org/wikipedia/commons/2/2b/Thibaut_Courtois_2018.jpg",
    "Marc-André ter Stegen": "https://upload.wikimedia.org/wikipedia/commons/2/2a/Marc-Andr%C3%A9_ter_Stegen_2021.jpg",
    "Gavi": "https://upload.wikimedia.org/wikipedia/commons/6/66/Gavi_2022.jpg",
    "Vinicius Junior": "https://upload.wikimedia.org/wikipedia/commons/5/5e/Vinicius_Junior_2022.jpg",
    "Mohamed Salah": "https://upload.wikimedia.org/wikipedia/commons/6/6a/Mohamed_Salah_2018.jpg",
    "Harry Kane": "https://upload.wikimedia.org/wikipedia/commons/0/09/Harry_Kane_2021.jpg",
    "Neymar": "https://upload.wikimedia.org/wikipedia/commons/0/0d/Neymar_2018.jpg",
    "Frenkie de Jong": "https://upload.wikimedia.org/wikipedia/commons/5/56/Frenkie_de_Jong_2021.jpg",
    "Lautaro Martinez": "https://upload.wikimedia.org/wikipedia/commons/6/67/Lautaro_Mart%C3%ADnez_2018.jpg",
    "Antoine Griezmann": "https://upload.wikimedia.org/wikipedia/commons/2/2d/Antoine_Griezmann_2021.jpg",
    "Martin Odegaard": "https://upload.wikimedia.org/wikipedia/commons/2/2f/Martin_%C3%98degaard_2021.jpg",
    "Bernardo Silva": "https://upload.wikimedia.org/wikipedia/commons/4/4a/Bernardo_Silva_2019.jpg",
    "Bukayo Saka": "https://upload.wikimedia.org/wikipedia/commons/0/09/Bukayo_Saka_2021.jpg",
    "Jamal Musiala": "https://upload.wikimedia.org/wikipedia/commons/1/19/Jamal_Musiala_2022.jpg",
    "Lamine Yamal": "https://upload.wikimedia.org/wikipedia/commons/4/4c/Lamine_Yamal_2024.jpg",
    "William Saliba": "https://upload.wikimedia.org/wikipedia/commons/2/2f/William_Saliba_2022.jpg",
    "Antonio Rudiger": "https://upload.wikimedia.org/wikipedia/commons/2/2c/Antonio_R%C3%BCdiger_2021.jpg",
    "Emiliano Martinez": "https://upload.wikimedia.org/wikipedia/commons/0/0d/Emiliano_Mart%C3%ADnez_2021.jpg",
    "Ederson": "https://upload.wikimedia.org/wikipedia/commons/6/6b/Ederson_2018.jpg",
}


ASSETS_DIR = Path(__file__).resolve().parent / "assets"
PLAYERS_ASSETS_DIR = ASSETS_DIR / "players"
TEAMS_ASSETS_DIR = ASSETS_DIR / "teams"
TRANSFERMARKT_DATA_PATH = ASSETS_DIR / "transfermarkt_squads.json"


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    lowered = normalized.lower()
    cleaned = re.sub(r"[^a-z0-9]+", "-", lowered).strip("-")
    return cleaned or "item"


def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _player_avatar_svg(player_name: str) -> str:
    initials = "".join([part[0] for part in player_name.split()[:2]]).upper() or "J"
    palette = ["#1E3A5F", "#2D5A87", "#6CABDD", "#A50044", "#C8102E", "#004170"]
    index = int(hashlib.md5(player_name.encode("utf-8")).hexdigest(), 16) % len(palette)
    bg = palette[index]
    return f"""
<svg xmlns='http://www.w3.org/2000/svg' width='256' height='256' viewBox='0 0 256 256'>
  <defs>
    <linearGradient id='g' x1='0' x2='1' y1='0' y2='1'>
      <stop offset='0%' stop-color='{bg}'/>
      <stop offset='100%' stop-color='#0f172a'/>
    </linearGradient>
  </defs>
  <rect width='256' height='256' rx='24' fill='url(#g)'/>
  <circle cx='128' cy='94' r='46' fill='rgba(255,255,255,0.16)'/>
  <rect x='58' y='148' width='140' height='66' rx='28' fill='rgba(255,255,255,0.14)'/>
  <text x='50%' y='56%' text-anchor='middle' fill='white'
        font-family='Arial, sans-serif' font-size='62' font-weight='700'>{initials}</text>
</svg>
""".strip()


def _team_logo_svg(team_name: str) -> str:
    color = TEAM_METADATA.get(team_name, {}).get("color", "#1E3A5F")
    initials = "".join([part[0] for part in team_name.split()[:2]]).upper() or "EQ"
    return f"""
<svg xmlns='http://www.w3.org/2000/svg' width='256' height='256' viewBox='0 0 256 256'>
  <rect width='256' height='256' rx='20' fill='{color}'/>
  <circle cx='128' cy='128' r='86' fill='rgba(255,255,255,0.16)'/>
  <text x='50%' y='55%' text-anchor='middle' fill='white'
        font-family='Arial, sans-serif' font-size='72' font-weight='700'>{initials}</text>
</svg>
""".strip()


def _ensure_local_player_avatar(player_name: str) -> Path:
    _ensure_dir(PLAYERS_ASSETS_DIR)
    avatar_path = PLAYERS_ASSETS_DIR / f"{slugify(player_name)}.svg"
    if not avatar_path.exists():
        avatar_path.write_text(_player_avatar_svg(player_name), encoding="utf-8")
    return avatar_path


def _existing_local_real_photo(player_name: str) -> Path | None:
    # First try explicit local static mapping.
    if player_name in PLAYER_IMAGE_URL:
        base = slugify(player_name)
        for ext in ("jpg", "jpeg", "png", "webp"):
            candidate = PLAYERS_ASSETS_DIR / f"{base}.{ext}"
            if candidate.exists():
                return candidate

    # Then try Transfermarkt dataset by normalized player name.
    tm_photo = _transfermarkt_local_photo(player_name)
    if tm_photo is not None:
        return tm_photo

    return None


def _name_key(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    lowered = normalized.lower()
    lowered = lowered.replace(" jr.", " junior").replace(" jr", " junior")
    lowered = lowered.replace(" martinez", " martinez").replace(" de ", " ")
    return re.sub(r"[^a-z0-9]+", "", lowered)


@lru_cache(maxsize=1)
def _transfermarkt_photo_index() -> dict[str, str]:
    index: dict[str, str] = {}
    if not TRANSFERMARKT_DATA_PATH.exists():
        return index
    try:
        data = json.loads(TRANSFERMARKT_DATA_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return index

    for players in data.values():
        for item in players:
            name = item.get("name", "")
            local_image = item.get("local_image", "")
            if not name or not local_image:
                continue
            image_path = Path(local_image)
            if image_path.exists():
                index[_name_key(name)] = str(image_path)
    return index


def _transfermarkt_local_photo(player_name: str) -> Path | None:
    index = _transfermarkt_photo_index()
    key = _name_key(player_name)
    path = index.get(key)
    if path:
        p = Path(path)
        if p.exists():
            return p

    # small aliases for known naming differences
    aliases = {
        "viniciusjr": "viniciusjunior",
        "lautaromartinez": "lautaro martinez",
    }
    alias_key = aliases.get(key)
    if alias_key:
        apath = index.get(_name_key(alias_key))
        if apath:
            p = Path(apath)
            if p.exists():
                return p

    base = slugify(player_name)
    for ext in ("jpg", "jpeg", "png", "webp"):
        candidate = PLAYERS_ASSETS_DIR / f"{base}.{ext}"
        if candidate.exists():
            return candidate
    return None


def player_image_path(player_name: str, use_real_when_available: bool = True) -> str:
    _ensure_dir(PLAYERS_ASSETS_DIR)
    if use_real_when_available:
        real_photo = _existing_local_real_photo(player_name)
        if real_photo is not None:
            return str(real_photo)
    return str(_ensure_local_player_avatar(player_name))


def team_logo(team_name: str) -> str:
    _ensure_dir(TEAMS_ASSETS_DIR)
    png_path = TEAMS_ASSETS_DIR / f"{slugify(team_name)}.png"
    if png_path.exists():
        return str(png_path)
    logo_path = TEAMS_ASSETS_DIR / f"{slugify(team_name)}.svg"
    if not logo_path.exists():
        logo_path.write_text(_team_logo_svg(team_name), encoding="utf-8")
    return str(logo_path)


def is_rival_player(team_name: str, player_name: str) -> bool:
    current_club = PLAYER_CLUB.get(player_name)
    if current_club is None:
        return False
    rivals = TEAM_METADATA.get(team_name, {}).get("rivals", set())
    return current_club in rivals


def team_description(team_name: str) -> str:
    return TEAM_METADATA.get(team_name, {}).get(
        "description", "Sin descripcion detallada para este equipo."
    )
