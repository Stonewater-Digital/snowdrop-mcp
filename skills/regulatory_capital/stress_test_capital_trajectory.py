"""
Executive Summary: Stress test capital path projecting CET1 ratio per quarter with PPNR, losses, and RWA dynamics.
Inputs: starting_cet1_capital (float), starting_rwa (float), quarterly_losses (list[float]), quarterly_ppnr (list[float]), rwa_growth_path_pct (list[float]), deferred_tax_assets (list[float])
Outputs: cet1_path (list[dict]), trough_ratio_pct (float), depletion_quarter (int)
MCP Tool Name: stress_test_capital_trajectory
"""
import logging
from datetime import datetime, timezone
from typing import Any, List

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "stress_test_capital_trajectory",
    "description": "Projects CET1 ratio quarter-by-quarter under supervisory stress inputs.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "starting_cet1_capital": {"type": "number", "description": "Starting CET1 capital."},
            "starting_rwa": {"type": "number", "description": "Starting risk-weighted assets."},
            "quarterly_losses": {
                "type": "array",
                "description": "Credit losses per quarter.",
                "items": {"type": "number"},
            },
            "quarterly_ppnr": {
                "type": "array",
                "description": "Pre-provision net revenue per quarter.",
                "items": {"type": "number"},
            },
            "rwa_growth_path_pct": {
                "type": "array",
                "description": "Percentage RWA change per quarter.",
                "items": {"type": "number"},
            },
            "deferred_tax_assets": {
                "type": "array",
                "description": "DTA write-down/add-back per quarter.",
                "items": {"type": "number"},
                "default": [],
            },
        },
        "required": [
            "starting_cet1_capital",
            "starting_rwa",
            "quarterly_losses",
            "quarterly_ppnr",
            "rwa_growth_path_pct",
        ],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "description": "status"},
            "data": {"type": "object", "description": "Capital trajectory"},
            "timestamp": {"type": "string", "description": "timestamp"},
        },
        "required": ["status", "timestamp"],
    },
}


def stress_test_capital_trajectory(
    starting_cet1_capital: float,
    starting_rwa: float,
    quarterly_losses: List[float],
    quarterly_ppnr: List[float],
    rwa_growth_path_pct: List[float],
    deferred_tax_assets: List[float] | None = None,
    **_: Any,
) -> dict[str, Any]:
    try:
        n = len(quarterly_losses)
        if not (len(quarterly_ppnr) == len(rwa_growth_path_pct) == n):
            raise ValueError("quarterly inputs must align")
        dta = deferred_tax_assets or [0.0] * n
        if len(dta) < n:
            dta += [0.0] * (n - len(dta))
        capital = starting_cet1_capital
        rwa = starting_rwa
        path = []
        trough_ratio = capital / rwa if rwa else 0.0
        trough_quarter = 0
        for quarter in range(n):
            capital += quarterly_ppnr[quarter] - quarterly_losses[quarter] + dta[quarter]
            rwa *= 1 + rwa_growth_path_pct[quarter] / 100.0
            ratio = capital / rwa if rwa else 0.0
            if ratio < trough_ratio:
                trough_ratio = ratio
                trough_quarter = quarter + 1
            path.append(
                {
                    "quarter": quarter + 1,
                    "capital": round(capital, 2),
                    "rwa": round(rwa, 2),
                    "cet1_ratio_pct": round(ratio * 100, 2),
                }
            )
        data = {
            "cet1_path": path,
            "trough_ratio_pct": round(trough_ratio * 100, 2),
            "depletion_quarter": trough_quarter,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"stress_test_capital_trajectory failed: {e}")
        _log_lesson(f"stress_test_capital_trajectory: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a", encoding="utf-8") as handle:
            handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
