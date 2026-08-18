from __future__ import annotations

import base64
import json
import mimetypes
from pathlib import Path

import pandas as pd
import streamlit as st

from prolog_bridge import (
    PrologBridgeError,
    analyze_combination,
    best_signing,
    best_signing_filtered,
    can_sign,
    list_players,
    list_teams,
    optimal_combination,
    optimal_combination_filtered,
    player_facts,
    recommendations,
    signing_breakdown,
    team_overview,
)
from visual_data import (
    PLAYER_CLUB,
    TEAM_METADATA,
    TRANSFERMARKT_DATA_PATH,
    is_rival_player,
    player_image_path,
    team_description,
    team_logo,
)

TOP20_TEAMS = [
    {"rank": 1, "team": "Real Madrid", "league": "LaLiga", "country": "España"},
    {"rank": 2, "team": "Manchester City", "league": "Premier League", "country": "Inglaterra"},
    {"rank": 3, "team": "Bayern Munich", "league": "Bundesliga", "country": "Alemania"},
    {"rank": 4, "team": "Barcelona", "league": "LaLiga", "country": "España"},
    {"rank": 5, "team": "PSG", "league": "Ligue 1", "country": "Francia"},
    {"rank": 6, "team": "Liverpool", "league": "Premier League", "country": "Inglaterra"},
    {"rank": 7, "team": "Arsenal", "league": "Premier League", "country": "Inglaterra"},
    {"rank": 8, "team": "Inter", "league": "Serie A", "country": "Italia"},
    {"rank": 9, "team": "Atletico Madrid", "league": "LaLiga", "country": "España"},
    {"rank": 10, "team": "Chelsea", "league": "Premier League", "country": "Inglaterra"},
    {"rank": 11, "team": "Juventus", "league": "Serie A", "country": "Italia"},
    {"rank": 12, "team": "Manchester United", "league": "Premier League", "country": "Inglaterra"},
    {"rank": 13, "team": "AC Milan", "league": "Serie A", "country": "Italia"},
    {"rank": 14, "team": "Borussia Dortmund", "league": "Bundesliga", "country": "Alemania"},
    {"rank": 15, "team": "Bayer Leverkusen", "league": "Bundesliga", "country": "Alemania"},
    {"rank": 16, "team": "Tottenham", "league": "Premier League", "country": "Inglaterra"},
    {"rank": 17, "team": "Napoli", "league": "Serie A", "country": "Italia"},
    {"rank": 18, "team": "RB Leipzig", "league": "Bundesliga", "country": "Alemania"},
    {"rank": 19, "team": "Benfica", "league": "Primeira Liga", "country": "Portugal"},
    {"rank": 20, "team": "Porto", "league": "Primeira Liga", "country": "Portugal"},
]

WORLD_ELITE_PLAYERS = [
    {"player": "Kylian Mbappé", "club": "Real Madrid", "rating": 91},
    {"player": "Rodri", "club": "Manchester City", "rating": 91},
    {"player": "Erling Haaland", "club": "Manchester City", "rating": 91},
    {"player": "Jude Bellingham", "club": "Real Madrid", "rating": 90},
    {"player": "Vinícius Jr.", "club": "Real Madrid", "rating": 90},
    {"player": "Kevin De Bruyne", "club": "Manchester City", "rating": 90},
    {"player": "Harry Kane", "club": "Bayern Munich", "rating": 90},
    {"player": "Mohamed Salah", "club": "Liverpool", "rating": 89},
    {"player": "Lautaro Martínez", "club": "Inter", "rating": 89},
    {"player": "Virgil van Dijk", "club": "Liverpool", "rating": 89},
]


st.set_page_config(
    page_title="Sistema de Fichajes (Prolog)",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
.hero {
  background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 70%, #0f172a 100%);
  color: #fff; border-radius: 14px; padding: 16px 18px; margin-bottom: 12px;
}
.hero h1 { margin: 0; font-size: 1.45rem; color: white !important; }
.hero p { margin: 4px 0 0 0; opacity: 0.92; }
.card {
  border: 1px solid rgba(100,116,139,.35);
  border-radius: 12px; padding: 10px 12px; margin-bottom: 10px;
  background: rgba(15,23,42,.03);
}
.pname { font-weight: 700; font-size: 1.02rem; margin-bottom: 2px; }
.pmeta { color: #64748b; font-size: .9rem; margin-bottom: 6px; }
.pimg {
  width: 96px; height: 96px; border-radius: 12px; object-fit: cover;
  border: 1px solid rgba(100,116,139,.35);
}
.logo {
  width: 82px; height: 82px; border-radius: 10px; object-fit: contain;
  border: 1px solid rgba(100,116,139,.25); padding: 6px;
}
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="hero">
  <h1>⚽ Sistema Lógico de Compra de Jugadores</h1>
  <p>Refactor visual estable para entrega: imágenes locales + análisis de fichajes sobre Prolog.</p>
</div>
""",
    unsafe_allow_html=True,
)


@st.cache_data(ttl=300)
def load_teams() -> list[str]:
    return list_teams()


@st.cache_data(ttl=300)
def load_players() -> list[str]:
    return list_players()


@st.cache_data(ttl=300)
def load_player_facts(players: tuple[str, ...]) -> list[dict]:
    return player_facts(list(players))


@st.cache_data(ttl=120)
def load_recommendations(team: str) -> list[dict]:
    rows = recommendations(team)
    return sorted(rows, key=lambda item: item["rendimiento"], reverse=True)


@st.cache_data(ttl=120)
def load_best_signing(team: str) -> dict:
    return best_signing(team)


@st.cache_data(ttl=120)
def load_optimal_combination(team: str) -> dict:
    return optimal_combination(team)


@st.cache_data(ttl=300)
def load_team_overview(team: str) -> dict:
    return team_overview(team)


@st.cache_data(ttl=300)
def load_transfermarkt_squads(_version: float) -> dict[str, list[dict]]:
    path = Path(TRANSFERMARKT_DATA_PATH)
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def get_transfermarkt_squads() -> dict[str, list[dict]]:
    path = Path(TRANSFERMARKT_DATA_PATH)
    version = path.stat().st_mtime if path.exists() else 0.0
    return load_transfermarkt_squads(version)


def _file_to_data_uri(path_str: str) -> str:
    if not path_str:
        return ""
    path = Path(path_str)
    if not path.exists() or path.is_dir():
        return ""
    data = path.read_bytes()
    mime = mimetypes.guess_type(str(path))[0] or "application/octet-stream"
    encoded = base64.b64encode(data).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def player_image_src(player: str, use_real_photos: bool) -> str:
    path = player_image_path(player, use_real_when_available=use_real_photos)
    return _file_to_data_uri(path)


def team_logo_src(team: str) -> str:
    return _file_to_data_uri(team_logo(team))


def rival_exclusions(team: str, players: list[str], enabled: bool) -> list[str]:
    if not enabled:
        return []
    return [player for player in players if is_rival_player(team, player)]


def same_team_exclusions(team: str, players: list[str], enabled: bool) -> list[str]:
    if not enabled:
        return []
    team_normalized = team.strip().lower()
    blocked: list[str] = []
    for player in players:
        club = str(PLAYER_CLUB.get(player, "")).strip().lower()
        if club and club == team_normalized:
            blocked.append(player)
    return blocked


def build_signing_explanation(
    team: str,
    player: str,
    breakdown: dict,
    overview: dict,
    allowed: bool,
    rival_flag: bool,
    same_team_flag: bool,
) -> list[str]:
    budget = int(overview.get("presupuesto", 0))
    price = int(breakdown.get("precio", 0))
    remaining = budget - price
    needed_positions = overview.get("necesidades", [])
    position = str(breakdown.get("posicion", "n/d"))

    notes = [
        f"Presupuesto: {price} M€ {'<=' if breakdown['puede_pagar'] else '>'} {budget} M€ (restante estimado: {remaining} M€).",
        f"Posición: {position} {'sí' if breakdown['cubre_posicion'] else 'no'} está dentro de necesidades {needed_positions}.",
        f"Edad: {'cumple' if breakdown['cumple_edad'] else 'no cumple'} restricciones del equipo.",
        f"Rivalidad: {'excluido por política de rivales' if rival_flag else 'sin bloqueo por rivalidad'}.",
        f"Mismo equipo: {'bloqueado (no transferencias internas)' if same_team_flag else 'permitido por origen de club'}.",
    ]
    if allowed and not rival_flag and not same_team_flag:
        notes.append(f"Veredicto: {team} puede fichar a {player} con las reglas actuales.")
    elif allowed and (rival_flag or same_team_flag):
        notes.append("Veredicto: lógicamente viable en Prolog, pero bloqueado por políticas activas del frontend.")
    else:
        notes.append(f"Veredicto: {team} no puede fichar a {player} con las restricciones actuales.")
    return notes


def team_selector_options(prolog_teams: list[str], squads: dict[str, list[dict]]) -> list[str]:
    ranked = [item["team"] for item in TOP20_TEAMS]
    seen = set()
    ordered: list[str] = []
    for name in ranked + list(squads.keys()) + prolog_teams:
        if name not in seen:
            ordered.append(name)
            seen.add(name)
    return ordered


def render_player_card(row: dict, facts_map: dict[str, dict], use_real_photos: bool) -> None:
    club = PLAYER_CLUB.get(row["jugador"], "Sin dato")
    facts = facts_map.get(row["jugador"], {})
    img_src = player_image_src(row["jugador"], use_real_photos)
    st.markdown(
        f"""
<div class="card">
  <div style="display:flex; gap:12px; align-items:flex-start;">
    <img class="pimg" src="{img_src}" />
    <div>
      <div class="pname">{row["jugador"]}</div>
      <div class="pmeta">{club} | {str(facts.get("nacionalidad", "n/d")).capitalize()} | {row["posicion"]}</div>
      <div>Rendimiento <strong>{row["rendimiento"]}</strong> · Precio <strong>{row["precio"]} M€</strong> · Edad <strong>{row["edad"]}</strong></div>
    </div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )


def render_transfermarkt_card(player: dict) -> None:
    img_src = _file_to_data_uri(player.get("local_image", ""))
    if not img_src:
        # Fallback seguro: avatar local por nombre si falta imagen descargada.
        img_src = player_image_src(player.get("name", "Jugador"), use_real_photos=True)
    profile = player.get("profile_url", "").strip()
    link_html = (
        f'<div><a href="{profile}" target="_blank">Abrir perfil en Transfermarkt</a></div>'
        if profile
        else '<div class="pmeta">Jugador agregado como referencia élite</div>'
    )
    st.markdown(
        f"""
<div class="card">
  <div style="display:flex; gap:12px; align-items:flex-start;">
    <img class="pimg" src="{img_src}" />
    <div>
      <div class="pname">{player.get("name", "Jugador")}</div>
      <div class="pmeta">ID TM: {player.get("player_id", "-")}</div>
      {link_html}
    </div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )


def render_top20_teams_and_elite_players(use_real_photos: bool) -> None:
    st.markdown("### Top 20 equipos del mundo")
    st.caption(
        "Listado curado para demo académica, apoyado en referencias públicas de Transfermarkt y rankings de rendimiento reciente."
    )
    df = pd.DataFrame(TOP20_TEAMS)
    st.dataframe(df, hide_index=True, width="stretch")
    st.markdown("#### Vista visual de equipos")
    for item in TOP20_TEAMS:
        logo = team_logo_src(item["team"])
        st.markdown(
            f"""
<div class="card">
  <div style="display:flex; gap:12px; align-items:center;">
    <img class="logo" src="{logo}" />
    <div>
      <div class="pname">#{item["rank"]} · {item["team"]}</div>
      <div class="pmeta">{item["league"]} · {item["country"]}</div>
    </div>
  </div>
</div>
""",
            unsafe_allow_html=True,
        )
    st.markdown(
        "Referencias: [Transfermarkt FC Barcelona](https://www.transfermarkt.com/fc-barcelona/startseite/verein/131) · "
        "[EA FC Ratings](https://www.ea.com/games/ea-sports-fc/ratings?orderBy=rank&page=163)"
    )

    st.markdown("### Jugadores élite globales (aunque no estén en esos 20 equipos)")
    for idx, item in enumerate(WORLD_ELITE_PLAYERS, start=1):
        img_src = player_image_src(item["player"], use_real_photos)
        st.markdown(
            f"""
<div class="card">
  <div style="display:flex; gap:12px; align-items:flex-start;">
    <img class="pimg" src="{img_src}" />
    <div>
      <div class="pname">#{idx} · {item["player"]}</div>
      <div class="pmeta">{item["club"]}</div>
      <div>Rating (EA FC): <strong>{item["rating"]}</strong></div>
    </div>
  </div>
</div>
""",
            unsafe_allow_html=True,
        )


def inject_elite_players_for_team(team: str, tm_players: list[dict]) -> list[dict]:
    existing = {str(item.get("name", "")).strip().lower() for item in tm_players}
    extra = []
    for item in WORLD_ELITE_PLAYERS:
        if item["club"] != team:
            continue
        if item["player"].strip().lower() in existing:
            continue
        extra.append(
            {
                "team": team,
                "player_id": f"elite-{item['player']}",
                "name": item["player"],
                "name_key": "",
                "profile_url": "",
                "image_url": "",
                "local_image": "",
            }
        )
    return tm_players + extra


def main() -> None:
    try:
        prolog_teams = load_teams()
        players = load_players()
    except PrologBridgeError as exc:
        st.error(f"No se pudo inicializar Prolog: {exc}")
        st.stop()

    squads = get_transfermarkt_squads()
    teams = team_selector_options(prolog_teams, squads)

    with st.sidebar:
        st.header("Opciones")
        st.caption("Selector global: Top 20 equipos + equipos modelados en Prolog.")
        team = st.selectbox("Equipo", teams)
        logo_src = team_logo_src(team)
        if logo_src:
            st.markdown(f'<img class="logo" src="{logo_src}" />', unsafe_allow_html=True)
        use_real_photos = st.toggle("Usar fotos locales reales", value=True)
        exclude_rivals = st.toggle("Excluir jugadores de rivales", value=True)
        block_same_team = st.toggle("Bloquear fichajes del mismo equipo", value=True)
        explain_mode = st.toggle("Modo explicación académica", value=True)
        if st.button("Limpiar caché y refrescar"):
            st.cache_data.clear()
            st.rerun()

    prolog_enabled = team in set(prolog_teams)
    tm_players = squads.get(team, [])
    rival_blocked = rival_exclusions(team, players, exclude_rivals) if prolog_enabled else []
    same_team_blocked = same_team_exclusions(team, players, block_same_team) if prolog_enabled else []
    excluded = sorted(set(rival_blocked + same_team_blocked))
    st.subheader(f"{team} · Panel")
    st.caption("Imágenes en local desde `frontend/assets/players` (sin depender de internet).")

    if prolog_enabled:
        st.success(
            "Equipo con modelo Prolog completo: habilita evaluación de fichaje, mejor fichaje, "
            "simulación multi-jugador y combinación óptima."
        )
    else:
        st.info(
            "Equipo en modo visual/dataset Top 20: muestra plantilla y métricas visuales, "
            "sin inferencia lógica completa de Prolog."
        )

    st.markdown(
        f"""
<div class="card">
  <strong>Perfil del equipo:</strong> {team_description(team)}
</div>
""",
        unsafe_allow_html=True,
    )

    if prolog_enabled:
        overview = load_team_overview(team)
        c1, c2, c3 = st.columns(3)
        c1.metric("Presupuesto (M€)", overview["presupuesto"])
        c2.metric("Cupo extranjeros", overview["cupo_extranjeros"])
        c3.metric("Nacionalidad base", str(overview["nacionalidad"]).capitalize())
        st.markdown(
            f"""
<div class="card">
  <span class="pmeta">Posiciones necesarias: {", ".join(overview["necesidades"])}</span>
</div>
""",
            unsafe_allow_html=True,
        )

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "Equipo seleccionado",
            "Análisis Prolog" if prolog_enabled else "Top 20 Equipos",
            "Galería Prolog" if prolog_enabled else "Jugadores élite",
            "Top 20 Equipos" if prolog_enabled else "Dataset",
        ]
    )

    with tab1:
        st.markdown("### Plantilla del equipo seleccionado")
        if not tm_players:
            st.warning(
                "No hay plantilla descargada para este equipo. Ejecuta `python3 frontend/prepare_assets.py`."
            )
        else:
            tm_players = inject_elite_players_for_team(team, tm_players)
            st.caption(f"Jugadores de plantilla disponibles: {len(tm_players)}")
            query = st.text_input("Buscar jugador de plantilla", key="tm_selected_search")
            display_players = tm_players
            if query.strip():
                term = query.strip().lower()
                display_players = [p for p in tm_players if term in str(p.get("name", "")).lower()]
            for player in display_players:
                render_transfermarkt_card(player)

    with tab2:
        if not prolog_enabled:
            render_top20_teams_and_elite_players(use_real_photos)
        else:
            st.markdown("### Evaluar un fichaje")
            selected = st.selectbox("Jugador", players)
            if st.button("Analizar fichaje", width="stretch"):
                breakdown = signing_breakdown(team, selected)
                allowed = can_sign(team, selected)
                rival_flag = selected in rival_blocked
                same_team_flag = selected in same_team_blocked
                blocked_by_policy = rival_flag or same_team_flag
                if allowed and not blocked_by_policy:
                    st.success(f"{team} puede fichar a {selected}.")
                elif allowed and blocked_by_policy:
                    reasons = []
                    if rival_flag:
                        reasons.append("rivalidad")
                    if same_team_flag:
                        reasons.append("mismo equipo")
                    st.warning(f"Cumple reglas, pero está bloqueado por política de: {', '.join(reasons)}.")
                else:
                    st.error("No cumple las reglas de fichaje.")

                b1, b2 = st.columns(2)
                b1.write(f"- Presupuesto: {'✅' if breakdown['puede_pagar'] else '❌'}")
                b1.write(f"- Posición: {'✅' if breakdown['cubre_posicion'] else '❌'}")
                b2.write(f"- Edad: {'✅' if breakdown['cumple_edad'] else '❌'}")
                b2.write(f"- Rivalidad: {'❌' if rival_flag else '✅'}")
                b2.write(f"- Mismo equipo: {'❌' if same_team_flag else '✅'}")

                if explain_mode:
                    st.markdown("#### Explicación formal de la decisión")
                    overview = load_team_overview(team)
                    explanation = build_signing_explanation(
                        team=team,
                        player=selected,
                        breakdown=breakdown,
                        overview=overview,
                        allowed=allowed,
                        rival_flag=rival_flag,
                        same_team_flag=same_team_flag,
                    )
                    for line in explanation:
                        st.write(f"- {line}")
                    with st.expander("Detalle técnico (JSON)"):
                        st.json(
                            {
                                "overview": overview,
                                "breakdown": breakdown,
                                "allowed": allowed,
                                "rival_filter": rival_flag,
                                "same_team_filter": same_team_flag,
                            }
                        )

            st.markdown("### Mejor fichaje sugerido")
            best = best_signing_filtered(team, excluded) if excluded else load_best_signing(team)
            if best.get("encontrado"):
                facts_map = {row["jugador"]: row for row in load_player_facts(tuple(players))}
                render_player_card(best, facts_map, use_real_photos)
            else:
                st.warning("No se encontró mejor fichaje.")

            st.markdown("### Combinación óptima")
            combo = optimal_combination_filtered(team, excluded) if excluded else load_optimal_combination(team)
            if combo.get("encontrada"):
                c4, c5, c6 = st.columns(3)
                c4.metric("Costo", combo["costo"])
                c5.metric("Rendimiento base", combo["rendimiento_base"])
                c6.metric("Rendimiento con química", round(combo["rendimiento_mejorado"], 2))
                st.write(", ".join(combo["jugadores"]))
            else:
                st.warning("No se encontró combinación válida.")

            st.markdown("### Simulador manual (múltiples jugadores)")
            st.caption(
                "Permite validar un paquete de fichajes contra presupuesto, cupos y reglas de liga. "
                "Útil cuando el presupuesto es alto y el análisis de 1 jugador queda corto."
            )
            selected_pack = st.multiselect(
                "Jugadores a evaluar en conjunto",
                players,
                default=[],
                key="manual_pack",
            )
            if st.button("Evaluar paquete de fichajes", width="stretch", key="eval_pack"):
                if not selected_pack:
                    st.warning("Selecciona al menos un jugador para simular.")
                else:
                    blocked_players = [p for p in selected_pack if p in excluded]
                    evaluation = analyze_combination(team, selected_pack)
                    if evaluation.get("encontrada"):
                        c7, c8, c9 = st.columns(3)
                        c7.metric("Costo total", evaluation["costo"])
                        c8.metric("Rendimiento base", evaluation["rendimiento_base"])
                        c9.metric("Rendimiento con química", round(evaluation["rendimiento_mejorado"], 2))

                        checks = [
                            ("Todos pueden firmar", evaluation.get("todos_pueden_firmar")),
                            ("Presupuesto", evaluation.get("presupuesto_ok")),
                            ("Cupo extranjeros", evaluation.get("cupo_ok")),
                            ("Reglas de liga", evaluation.get("liga_ok")),
                            ("Combinación válida", evaluation.get("valida")),
                        ]
                        for label, ok in checks:
                            st.write(f"- {label}: {'✅' if ok else '❌'}")

                        if blocked_players:
                            st.warning(
                                "Políticas activas del frontend detectan bloqueos en: "
                                + ", ".join(blocked_players)
                                + ". La simulación Prolog se muestra igual para análisis académico."
                            )
                        else:
                            st.success("El paquete no tiene bloqueos de políticas en frontend.")
                    else:
                        st.error("No se pudo evaluar el paquete seleccionado.")

    with tab3:
        if not prolog_enabled:
            st.markdown("### Jugadores élite globales")
            for idx, item in enumerate(WORLD_ELITE_PLAYERS, start=1):
                img_src = player_image_src(item["player"], use_real_photos)
                st.markdown(
                    f"""
<div class="card">
  <div style="display:flex; gap:12px; align-items:flex-start;">
    <img class="pimg" src="{img_src}" />
    <div>
      <div class="pname">#{idx} · {item["player"]}</div>
      <div class="pmeta">{item["club"]}</div>
      <div>Rating (EA FC): <strong>{item["rating"]}</strong></div>
    </div>
  </div>
</div>
""",
                    unsafe_allow_html=True,
                )
        else:
            st.markdown("### Galería completa (jugadores del modelo Prolog)")
            facts = load_player_facts(tuple(players))
            df = pd.DataFrame(facts)
            text = st.text_input("Buscar por nombre")
            positions = sorted(df["posicion"].dropna().unique().tolist())
            selected_positions = st.multiselect("Posiciones", positions, default=positions)
            filtered = df[df["posicion"].isin(selected_positions)]
            if text.strip():
                filtered = filtered[filtered["jugador"].str.lower().str.contains(text.strip().lower())]
            filtered = filtered.sort_values(by=["rendimiento", "precio"], ascending=[False, True])
            facts_map = {row["jugador"]: row for row in facts}
            st.caption(f"Jugadores mostrados: {len(filtered)}")
            for row in filtered.to_dict(orient="records"):
                render_player_card(row, facts_map, use_real_photos)

    with tab4:
        render_top20_teams_and_elite_players(use_real_photos)


if __name__ == "__main__":
    main()
