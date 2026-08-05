from __future__ import annotations

import csv
import statistics
import time
from pathlib import Path

import sys

ROOT = Path(__file__).resolve().parents[1]
FRONTEND = ROOT / "frontend"
if str(FRONTEND) not in sys.path:
    sys.path.insert(0, str(FRONTEND))

from prolog_bridge import (  # noqa: E402
    best_signing,
    optimal_combination,
    recommendations,
)


OUT_CSV = ROOT / "benchmarks" / "latest_benchmark.csv"
OUT_MD = ROOT / "benchmarks" / "latest_benchmark.md"

TEAMS = [
    "Real Madrid",
    "Barcelona",
    "Manchester City",
    "Bayern Munich",
    "PSG",
    "Liverpool",
]


def measure_ms(fn, repeats: int = 5) -> list[float]:
    samples: list[float] = []
    for _ in range(repeats):
        start = time.perf_counter()
        fn()
        elapsed = (time.perf_counter() - start) * 1000
        samples.append(elapsed)
    return samples


def run() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for team in TEAMS:
        cases = [
            ("recommendations", lambda t=team: recommendations(t)),
            ("best_signing", lambda t=team: best_signing(t)),
            ("optimal_combination", lambda t=team: optimal_combination(t)),
        ]
        for query_name, fn in cases:
            samples = measure_ms(fn, repeats=5)
            rows.append(
                {
                    "team": team,
                    "query": query_name,
                    "runs": len(samples),
                    "min_ms": round(min(samples), 2),
                    "median_ms": round(statistics.median(samples), 2),
                    "max_ms": round(max(samples), 2),
                }
            )
    return rows


def write_csv(rows: list[dict[str, object]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    fields = ["team", "query", "runs", "min_ms", "median_ms", "max_ms"]
    with OUT_CSV.open("w", newline="", encoding="utf-8") as fp:
        writer = csv.DictWriter(fp, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(rows: list[dict[str, object]]) -> None:
    lines = [
        "# Benchmark de consultas Prolog",
        "",
        "Medición local en milisegundos (5 corridas por consulta).",
        "",
        "| Equipo | Consulta | Corridas | Min (ms) | Mediana (ms) | Max (ms) |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            f"| {row['team']} | {row['query']} | {row['runs']} | {row['min_ms']} | {row['median_ms']} | {row['max_ms']} |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    results = run()
    write_csv(results)
    write_markdown(results)
    print(f"Benchmark generado en: {OUT_CSV}")
    print(f"Resumen markdown: {OUT_MD}")
