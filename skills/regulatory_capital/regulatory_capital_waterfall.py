"""
Executive Summary: Capital ratio waterfall from CET1 through AT1 to Tier 2 with regulatory deductions.
Inputs: gross_cet1 (float), regulatory_deductions (float), at1_instruments (float), tier2_instruments (float), rwa (float)
Outputs: cet1_ratio (float), tier1_ratio (float), total_capital_ratio (float), buffers (dict)
MCP Tool Name: regulatory_capital_waterfall
"""
import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "regulatory_capital_waterfall",
    "description": "Applies deductions to CET1 and adds AT1/Tier2 to produce regulatory ratios.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "gross_cet1": {"type": "number", "description": "Gross CET1 capital before deductions."},
            "regulatory_deductions": {"type": "number", "description": "Total deductions (goodwill, DTAs, etc.)."},
            "at1_instruments": {"type": "number", "description": "Eligible AT1 capital."},
            "tier2_instruments": {"type": "number", "description": "Eligible Tier 2 capital."},
            "rwa": {"type": "number", "description": "Risk-weighted assets."},
        },
        "required": ["gross_cet1", "regulatory_deductions", "at1_instruments", "tier2_instruments", "rwa"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "description": "status"},
            "data": {"type": "object", "description": "Capital ratios"},
            "timestamp": {"type": "string", "description": "timestamp"},
        },
        "required": ["status", "timestamp"],
    },
}


def regulatory_capital_waterfall(
    gross_cet1: float,
    regulatory_deductions: float,
    at1_instruments: float,
    tier2_instruments: float,
    rwa: float,
    **_: Any,
) -> dict[str, Any]:
    try:
        cet1 = max(gross_cet1 - regulatory_deductions, 0.0)
        tier1 = cet1 + at1_instruments
        total_capital = tier1 + tier2_instruments
        ratios = {
            "cet1_ratio_pct": round((cet1 / rwa) * 100 if rwa else 0.0, 2),
            "tier1_ratio_pct": round((tier1 / rwa) * 100 if rwa else 0.0, 2),
            "total_capital_ratio_pct": round((total_capital / rwa) * 100 if rwa else 0.0, 2),
        }
        buffers = {
            "cet1_excess_pct": round(ratios["cet1_ratio_pct"] - 4.5, 2),
            "tier1_excess_pct": round(ratios["tier1_ratio_pct"] - 6.0, 2),
            "total_capital_excess_pct": round(ratios["total_capital_ratio_pct"] - 8.0, 2),
        }
        data = {
            "ratios": ratios,
            "capital_stack": {
                "cet1": round(cet1, 2),
                "tier1": round(tier1, 2),
                "total_capital": round(total_capital, 2),
            },
            "buffers": buffers,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"regulatory_capital_waterfall failed: {e}")
        _log_lesson(f"regulatory_capital_waterfall: {e}")
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
