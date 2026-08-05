from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FRONTEND = ROOT / "frontend"
if str(FRONTEND) not in sys.path:
    sys.path.insert(0, str(FRONTEND))

from prolog_bridge import (  # noqa: E402
    best_signing,
    list_players,
    list_teams,
    optimal_combination,
    signing_breakdown,
    team_overview,
)


class PrologBridgeSmokeTest(unittest.TestCase):
    def test_list_teams_has_expected_core(self) -> None:
        teams = list_teams()
        self.assertIn("Real Madrid", teams)
        self.assertIn("Barcelona", teams)
        self.assertGreaterEqual(len(teams), 6)

    def test_list_players_not_empty(self) -> None:
        players = list_players()
        self.assertIn("Kylian Mbappé", players)
        self.assertGreaterEqual(len(players), 50)

    def test_team_overview_shape(self) -> None:
        overview = team_overview("Real Madrid")
        self.assertEqual(overview["presupuesto"], 200)
        self.assertIn("delantero", overview["necesidades"])

    def test_signing_breakdown_has_expected_keys(self) -> None:
        breakdown = signing_breakdown("Real Madrid", "Robert Lewandowski")
        expected = {"puede_pagar", "cubre_posicion", "cumple_edad", "es_extranjero", "precio", "posicion", "edad"}
        self.assertTrue(expected.issubset(set(breakdown.keys())))

    def test_best_signing_exists(self) -> None:
        best = best_signing("Barcelona")
        self.assertTrue(best.get("encontrado"))
        self.assertIn("jugador", best)

    def test_optimal_combination_exists(self) -> None:
        combo = optimal_combination("Manchester City")
        self.assertTrue(combo.get("encontrada"))
        self.assertGreater(len(combo.get("jugadores", [])), 0)


if __name__ == "__main__":
    unittest.main()
