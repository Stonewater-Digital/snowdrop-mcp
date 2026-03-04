"""
Execuve Summary: Values equity using a two-stage dividend discount model.
Inputs: current_dividend (float), high_growth_rate (float), high_growth_years (int), terminal_growth_rate (float), required_return (float)
Outputs: intrinsic_value (float), high_growth_pv (float), terminal_pv (float), terminal_pv_pct (float)
MCP Tool Name: two_stage_ddm
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "two_stage_ddm",
    "description": "Discounts dividends through a high-growth phase and a terminal perpetuity.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "current_dividend": {"type": "number", "description": "Most recent dividend per share."},
            "high_growth_rate": {"type": "number", "description": "Growth rate during stage 1 (decimal)."},
            "high_growth_years": {"type": "integer", "description": "Years of high growth."},
            "terminal_growth_rate": {"type": "number", "description": "Perpetual growth rate after stage 1."},
            "required_return": {"type": "number", "description": "Discount rate."}
        },
        "required": ["current_dividend", "high_growth_rate", "high_growth_years", "terminal_growth_rate", "required_return"]
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "timestamp": {"type": "string"}, "data": {"type": "object"}}, "required": ["status", "timestamp"]
    }
}


def two_stage_ddm(**kwargs: Any) -> dict:
    """Discounts high-growth dividends and terminal value to estimate intrinsic price."""
    try:
        dividend = kwargs.get("current_dividend")
        g1 = kwargs.get("high_growth_rate")
        years = kwargs.get("high_growth_years")
        g_terminal = kwargs.get("terminal_growth_rate")
        required = kwargs.get("required_return")
        for label, value in (("current_dividend", dividend), ("high_growth_rate", g1), ("terminal_growth_rate", g_terminal), ("required_return", required)):
            if not isinstance(value, (int, float)):
                raise ValueError(f"{label} must be numeric")
        if not isinstance(years, int) or years <= 0:
            raise ValueError("high_growth_years must be positive integer")
        if required <= g_terminal:
            raise ValueError("required_return must exceed terminal growth")

        dividends = []
        for year in range(1, years + 1):
            dividend = dividend * (1 + g1)
            dividends.append(dividend)
        high_growth_pv = sum(dividends[year - 1] / ((1 + required) ** year) for year in range(1, years + 1))
        terminal_dividend = dividends[-1] * (1 + g_terminal)
        terminal_value = terminal_dividend / (required - g_terminal)
        terminal_pv = terminal_value / ((1 + required) ** years)
        intrinsic_value = high_growth_pv + terminal_pv
        terminal_pct = terminal_pv / intrinsic_value if intrinsic_value else 0.0

        return {
            "status": "success",
            "data": {
                "intrinsic_value": intrinsic_value,
                "high_growth_pv": high_growth_pv,
                "terminal_pv": terminal_pv,
                "terminal_pv_pct": terminal_pct
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"two_stage_ddm failed: {e}")
        _log_lesson(f"two_stage_ddm: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
