"""
Executive Summary: CCAR/DFAST capital trajectory projecting CET1 through losses, PPNR, and RWA growth.
Inputs: starting_capital (dict), projected_losses (list[float]), ppnr (list[float]), rwa_growth_pct (float)
Outputs: min_cet1_ratio (float), stress_capital_buffer (float), capital_path (list[dict])
MCP Tool Name: ccar_capital_planning
"""
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "ccar_capital_planning",
    "description": "Projects CET1 ratio over stress horizon using Fed CCAR methodology.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "starting_capital": {
                "type": "object",
                "description": "Starting CET1 capital and RWA.",
                "properties": {
                    "cet1_capital": {"type": "number", "description": "CET1 capital amount"},
                    "rwa": {"type": "number", "description": "Risk-weighted assets"},
                    "cet1_ratio_pct": {"type": "number", "description": "Reported CET1 ratio"},
                },
                "required": ["cet1_capital", "rwa"],
            },
            "projected_losses": {
                "type": "array",
                "description": "Quarterly losses over the stress horizon.",
                "items": {"type": "number"},
            },
            "ppnr": {
                "type": "array",
                "description": "Pre-provision net revenue per quarter.",
                "items": {"type": "number"},
            },
            "dividend_schedule": {
                "type": "array",
                "description": "Planned dividend distributions per quarter.",
                "items": {"type": "number"},
                "default": [],
            },
            "rwa_growth_pct": {
                "type": "number",
                "description": "Percentage growth in RWA per quarter.",
            },
            "buffer_requirement_pct": {
                "type": "number",
                "description": "Combined buffer requirement (default 4.5+buffers).",
                "default": 7.0,
            },
        },
        "required": ["starting_capital", "projected_losses", "ppnr", "rwa_growth_pct"],
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


def ccar_capital_planning(
    starting_capital: Dict[str, float],
    projected_losses: List[float],
    ppnr: List[float],
    rwa_growth_pct: float,
    dividend_schedule: List[float] | None = None,
    buffer_requirement_pct: float = 7.0,
    **_: Any,
) -> dict[str, Any]:
    try:
        if len(projected_losses) != len(ppnr):
            raise ValueError("projected_losses and ppnr must align in length")
        capital = starting_capital["cet1_capital"]
        rwa = starting_capital["rwa"]
        dividends = dividend_schedule or []
        if len(dividends) < len(projected_losses):
            dividends = dividends + [0.0] * (len(projected_losses) - len(dividends))
        elif len(dividends) > len(projected_losses):
            dividends = dividends[: len(projected_losses)]
        capital_path = []
        min_ratio = capital / rwa
        for quarter, (loss, revenue, dividend) in enumerate(zip(projected_losses, ppnr, dividends), start=1):
            capital += revenue - loss - dividend
            rwa *= 1 + rwa_growth_pct / 100.0
            ratio = capital / rwa if rwa else 0.0
            min_ratio = min(min_ratio, ratio)
            capital_path.append(
                {
                    "quarter": quarter,
                    "capital": round(capital, 2),
                    "rwa": round(rwa, 2),
                    "cet1_ratio_pct": round(ratio * 100, 2),
                }
            )
        buffer = (capital / rwa) * 100 - buffer_requirement_pct if rwa else 0.0
        stress_capital_buffer = max(starting_capital.get("cet1_ratio_pct", min_ratio * 100) - min_ratio * 100, 0.0)
        data = {
            "capital_path": capital_path,
            "minimum_cet1_ratio_pct": round(min_ratio * 100, 2),
            "ending_cet1_ratio_pct": round((capital / rwa) * 100, 2) if rwa else 0.0,
            "stress_capital_buffer_pct": round(stress_capital_buffer, 2),
            "buffer_headroom_pct": round(buffer, 2),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"ccar_capital_planning failed: {e}")
        _log_lesson(f"ccar_capital_planning: {e}")
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
