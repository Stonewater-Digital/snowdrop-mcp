"""
Executive Summary: Solvency II Minimum Capital Requirement applying linear formula and SCR-based floor/cap.
Inputs: technical_provisions (float), written_premiums (float), scr (float)
Outputs: mcr (float), floor (float), cap (float), compliance_status (str)
MCP Tool Name: solvency_ii_mcr
"""
import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "solvency_ii_mcr",
    "description": "Derives MCR using Solvency II linear formula (Life + Non-life) and SCR floor/cap.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "technical_provisions": {"type": "number", "description": "Net technical provisions."},
            "written_premiums": {"type": "number", "description": "Net written premiums of last 12 months."},
            "scr": {"type": "number", "description": "Solvency capital requirement."},
        },
        "required": ["technical_provisions", "written_premiums", "scr"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "description": "status"},
            "data": {"type": "object", "description": "MCR output"},
            "timestamp": {"type": "string", "description": "timestamp"},
        },
        "required": ["status", "timestamp"],
    },
}


def solvency_ii_mcr(
    technical_provisions: float,
    written_premiums: float,
    scr: float,
    **_: Any,
) -> dict[str, Any]:
    try:
        linear_mcr = 0.085 * technical_provisions + 0.25 * written_premiums
        floor = 0.25 * scr
        cap = 0.45 * scr
        mcr = min(max(linear_mcr, floor), cap)
        compliance = "compliant" if scr >= mcr else "breach"
        data = {
            "linear_mcr": round(linear_mcr, 2),
            "floor": round(floor, 2),
            "cap": round(cap, 2),
            "mcr": round(mcr, 2),
            "compliance_status": compliance,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"solvency_ii_mcr failed: {e}")
        _log_lesson(f"solvency_ii_mcr: {e}")
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
