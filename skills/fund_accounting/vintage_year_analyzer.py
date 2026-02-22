"""Analyze fund performance by vintage year."""
from __future__ import annotations

from statistics import mean, median
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "vintage_year_analyzer",
    "description": "Compares funds across vintages and computes quartiles/PME proxies.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "funds": {"type": "array", "items": {"type": "object"}},
        },
        "required": ["funds"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {"type": "object"},
            "timestamp": {"type": "string"},
        },
    },
}


def vintage_year_analyzer(funds: list[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Return vintage comparison stats and quartile rankings."""
    try:
        vintages: dict[int, list[dict[str, Any]]] = {}
        for fund in funds:
            year = int(fund.get("vintage_year", 0))
            vintages.setdefault(year, []).append(fund)
        comparison = []
        quartile_cutoffs: dict[int, dict[str, float]] = {}
        fund_rankings = []
        for year, bucket in sorted(vintages.items()):
            irr_values = [fund.get("irr", 0.0) for fund in bucket]
            tvpi_values = [fund.get("tvpi", 0.0) for fund in bucket]
            comparison.append(
                {
                    "vintage_year": year,
                    "median_irr": round(median(irr_values), 3),
                    "mean_irr": round(mean(irr_values), 3),
                    "median_tvpi": round(median(tvpi_values), 3),
                    "funds": len(bucket),
                }
            )
            sorted_irr = sorted(irr_values)
            q1 = sorted_irr[int(0.25 * (len(sorted_irr) - 1))]
            q3 = sorted_irr[int(0.75 * (len(sorted_irr) - 1))]
            quartile_cutoffs[year] = {"q1": q1, "q3": q3}
            for fund in bucket:
                status = "middle"
                irr = fund.get("irr", 0.0)
                if irr >= q3:
                    status = "top_quartile"
                elif irr <= q1:
                    status = "bottom_quartile"
                fund_rankings.append(
                    {"fund_name": fund.get("fund_name"), "vintage_year": year, "irr": irr, "quartile": status}
                )
        best_vintage = max(comparison, key=lambda item: item["median_irr"], default={}).get("vintage_year")
        worst_vintage = min(comparison, key=lambda item: item["median_irr"], default={}).get("vintage_year")
        data = {
            "vintage_comparison": comparison,
            "best_vintage": best_vintage,
            "worst_vintage": worst_vintage,
            "quartile_cutoffs": quartile_cutoffs,
            "fund_rankings": fund_rankings,
            "public_market_equivalent": None,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("vintage_year_analyzer", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
