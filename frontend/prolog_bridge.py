import json
import subprocess
from pathlib import Path
from typing import Any


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
CONOCIMIENTO_PATH = SRC_DIR / "conocimiento.pl"
REGLAS_PATH = SRC_DIR / "reglas.pl"


class PrologBridgeError(RuntimeError):
    """Error raised when SWI-Prolog execution fails."""


def _quote_atom(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace("'", "\\'")
    return f"'{escaped}'"


def _run_prolog_json(goal: str) -> Any:
    bootstrap = ",".join(
        [
            f"consult({_quote_atom(str(CONOCIMIENTO_PATH))})",
            f"consult({_quote_atom(str(REGLAS_PATH))})",
            "use_module(library(http/json))",
            goal,
        ]
    )

    command = ["swipl", "-q", "-f", "none", "-g", bootstrap, "-t", "halt"]
    try:
        result = subprocess.run(
            command,
            cwd=str(ROOT_DIR),
            capture_output=True,
            text=True,
            check=False,
            timeout=15,
        )
    except FileNotFoundError as exc:
        raise PrologBridgeError(
            "No se encontro el ejecutable 'swipl'. Instala SWI-Prolog para usar el frontend."
        ) from exc
    except subprocess.TimeoutExpired as exc:
        raise PrologBridgeError(
            "La consulta a Prolog excedio el tiempo limite (15s)."
        ) from exc

    if result.returncode != 0:
        stderr = result.stderr.strip() or "Error desconocido al ejecutar SWI-Prolog."
        raise PrologBridgeError(stderr)

    payload = result.stdout.strip()
    if not payload:
        raise PrologBridgeError("SWI-Prolog no devolvio salida para la consulta.")

    try:
        return json.loads(payload)
    except json.JSONDecodeError as exc:
        raise PrologBridgeError(
            "No se pudo interpretar la respuesta JSON de Prolog."
        ) from exc


def _list_as_prolog(players: list[str]) -> str:
    items = ",".join(_quote_atom(player) for player in players)
    return f"[{items}]"


def list_teams() -> list[str]:
    data = _run_prolog_json(
        "findall(E,presupuesto(E,_),Equipos0),sort(Equipos0,Equipos),json_write_dict(current_output,_{equipos:Equipos})"
    )
    return data["equipos"]


def list_players() -> list[str]:
    data = _run_prolog_json(
        "findall(J,jugador(J,_,_,_,_,_,_),J0),sort(J0,Jugadores),json_write_dict(current_output,_{jugadores:Jugadores})"
    )
    return data["jugadores"]


def team_overview(team: str) -> dict[str, Any]:
    team_atom = _quote_atom(team)
    goal = (
        f"presupuesto({team_atom},Presupuesto),"
        f"cupo_extranjeros({team_atom},Cupo),"
        f"nacionalidad_equipo({team_atom},Nacionalidad),"
        f"findall(Pos,necesita({team_atom},Pos),Necesidades),"
        "json_write_dict(current_output,_{presupuesto:Presupuesto,cupo_extranjeros:Cupo,nacionalidad:Nacionalidad,necesidades:Necesidades})"
    )
    return _run_prolog_json(goal)


def can_sign(team: str, player: str) -> bool:
    team_atom = _quote_atom(team)
    player_atom = _quote_atom(player)
    goal = (
        f"(puede_firmar({team_atom},{player_atom}) -> "
        "json_write_dict(current_output,_{puede_firmar:true}) ; "
        "json_write_dict(current_output,_{puede_firmar:false}))"
    )
    return bool(_run_prolog_json(goal)["puede_firmar"])


def recommendations(team: str) -> list[dict[str, Any]]:
    team_atom = _quote_atom(team)
    goal = (
        "findall(_{jugador:J,posicion:Pos,edad:Edad,precio:Precio,rendimiento:R},"
        f"(puede_firmar({team_atom},J),"
        " posicion_jugador(J,Pos),edad_jugador(J,Edad),precio_jugador(J,Precio),rendimiento(J,R)),"
        "Lista),"
        "json_write_dict(current_output,_{resultados:Lista})"
    )
    return _run_prolog_json(goal)["resultados"]


def player_facts(players: list[str]) -> list[dict[str, Any]]:
    if not players:
        return []

    prolog_list = _list_as_prolog(players)
    goal = (
        f"findall(_{{jugador:J,posicion:Pos,edad:Edad,precio:Precio,nacionalidad:Nac,goles:G,asistencias:A,rendimiento:R}},"
        f"(member(J,{prolog_list}),jugador(J,Pos,Edad,Precio,Nac,G,A),R is G+A),"
        "Lista),json_write_dict(current_output,_{resultados:Lista})"
    )
    return _run_prolog_json(goal)["resultados"]


def best_signing(team: str) -> dict[str, Any]:
    team_atom = _quote_atom(team)
    goal = (
        f"(mejor_fichaje({team_atom},J) -> "
        "posicion_jugador(J,Pos),edad_jugador(J,Edad),precio_jugador(J,Precio),rendimiento(J,R),"
        "json_write_dict(current_output,_{encontrado:true,jugador:J,posicion:Pos,edad:Edad,precio:Precio,rendimiento:R}) ; "
        "json_write_dict(current_output,_{encontrado:false}))"
    )
    return _run_prolog_json(goal)


def best_signing_filtered(team: str, excluded_players: list[str]) -> dict[str, Any]:
    team_atom = _quote_atom(team)
    excluded = _list_as_prolog(excluded_players)
    goal = (
        f"(mejor_fichaje_filtrado({team_atom},{excluded},J) -> "
        "posicion_jugador(J,Pos),edad_jugador(J,Edad),precio_jugador(J,Precio),"
        "jugador(J,_,_,_,Nac,_,_),rendimiento(J,R),"
        "json_write_dict(current_output,_{encontrado:true,jugador:J,posicion:Pos,edad:Edad,precio:Precio,nacionalidad:Nac,rendimiento:R}) ; "
        "json_write_dict(current_output,_{encontrado:false}))"
    )
    return _run_prolog_json(goal)


def optimal_combination(team: str) -> dict[str, Any]:
    team_atom = _quote_atom(team)
    goal = (
        f"(combinacion_optima({team_atom},Lista),"
        f"analizar_combinacion(Lista,{team_atom},Analisis) -> "
        "member(costo=Costo,Analisis),"
        "member(rendimiento_base=RBase,Analisis),"
        "member(rendimiento_mejorado=RMejorado,Analisis),"
        "member(quimica_total=Quimica,Analisis),"
        "member(extranjeros=Extranjeros,Analisis),"
        "member(cantera=Cantera,Analisis),"
        "json_write_dict(current_output,_{encontrada:true,jugadores:Lista,costo:Costo,rendimiento_base:RBase,rendimiento_mejorado:RMejorado,quimica_total:Quimica,extranjeros:Extranjeros,cantera:Cantera}) ; "
        "json_write_dict(current_output,_{encontrada:false}))"
    )
    return _run_prolog_json(goal)


def optimal_combination_filtered(team: str, excluded_players: list[str]) -> dict[str, Any]:
    team_atom = _quote_atom(team)
    excluded = _list_as_prolog(excluded_players)
    goal = (
        f"(combinacion_optima_filtrada({team_atom},{excluded},Lista),"
        f"analizar_combinacion(Lista,{team_atom},Analisis) -> "
        "member(costo=Costo,Analisis),"
        "member(rendimiento_base=RBase,Analisis),"
        "member(rendimiento_mejorado=RMejorado,Analisis),"
        "member(quimica_total=Quimica,Analisis),"
        "member(extranjeros=Extranjeros,Analisis),"
        "member(cantera=Cantera,Analisis),"
        "json_write_dict(current_output,_{encontrada:true,jugadores:Lista,costo:Costo,rendimiento_base:RBase,rendimiento_mejorado:RMejorado,quimica_total:Quimica,extranjeros:Extranjeros,cantera:Cantera}) ; "
        "json_write_dict(current_output,_{encontrada:false}))"
    )
    return _run_prolog_json(goal)


def signing_breakdown(team: str, player: str) -> dict[str, Any]:
    team_atom = _quote_atom(team)
    player_atom = _quote_atom(player)
    goal = (
        f"(puede_pagar({team_atom},{player_atom}) -> Pagar=true ; Pagar=false),"
        f"(juega_posicion_necesaria({player_atom},{team_atom}) -> Posicion=true ; Posicion=false),"
        f"(cumple_restricciones_edad({player_atom},{team_atom}) -> Edad=true ; Edad=false),"
        f"(es_extranjero({player_atom},{team_atom}) -> Extranjero=true ; Extranjero=false),"
        f"precio_jugador({player_atom},Precio),"
        f"posicion_jugador({player_atom},Pos),"
        f"edad_jugador({player_atom},EdadJugador),"
        "json_write_dict(current_output,_{puede_pagar:Pagar,cubre_posicion:Posicion,cumple_edad:Edad,es_extranjero:Extranjero,precio:Precio,posicion:Pos,edad:EdadJugador})"
    )
    return _run_prolog_json(goal)


def chemistry_between(player_a: str, player_b: str) -> int:
    a_atom = _quote_atom(player_a)
    b_atom = _quote_atom(player_b)
    goal = (
        f"quimica_entre({a_atom},{b_atom},Q),"
        "json_write_dict(current_output,_{quimica:Q})"
    )
    return int(_run_prolog_json(goal)["quimica"])
