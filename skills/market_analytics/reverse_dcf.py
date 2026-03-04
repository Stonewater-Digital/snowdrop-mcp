"""
Execuve Summary: Solves for the growth rate embedded in a market price via reverse DCF.
Inputs: market_cap (float), current_fcf (float), wacc (float), terminal_growth (float), projection_years (int|None)
Outputs: implied_growth_rate (float), implied_growth_years (int), reasonableness_check (str), vs_historical_growth (str)
MCP Tool Name: reverse_dcf
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "reverse_dcf",
    "description": "Derives the growth rate required to justify the current market capitalization.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "market_cap": {"type": "number", "description": "Current enterprise/market value."},
            "current_fcf": {"type": "number", "description": "Last-twelve-month free cash flow."},
            "wacc": {"type": "number", "description": "Discount rate."},
            "terminal_growth": {"type": "number", "description": "Perpetual growth used in terminal value."},
            "projection_years": {"type": "integer", "description": "Years of explicit growth (default 5)."}
        },
        "required": ["market_cap", "current_fcf", "wacc", "terminal_growth"]
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "timestamp": {"type": "string"}, "data": {"type": "object"}}, "required": ["status", "timestamp"]
    }
}


def reverse_dcf(**kwargs: Any) -> dict:
    """Uses binary search to find growth rate implied by market value."""
    try:
        market_cap = kwargs.get("market_cap")
        current_fcf = kwargs.get("current_fcf")
        wacc = kwargs.get("wacc")
        terminal_growth = kwargs.get("terminal_growth")
        years = kwargs.get("projection_years") or 5
        for label, value in (("market_cap", market_cap), ("current_fcf", current_fcf), ("wacc", wacc), ("terminal_growth", terminal_growth)):
            if not isinstance(value, (int, float)):
                raise ValueError(f"{label} must be numeric")
        if wacc <= terminal_growth:
            raise ValueError("wacc must exceed terminal growth")

        def _dcf(growth: float) -> float:
            fcf = current_fcf
            pv = 0.0
            for year in range(1, years + 1):
                fcf *= (1 + growth)
                pv += fcf / ((1 + wacc) ** year)
            terminal_fcf = fcf * (1 + terminal_growth)
            terminal_value = terminal_fcf / (wacc - terminal_growth)
            pv += terminal_value / ((1 + wacc) ** years)
            return pv

        low, high = -0.5, 1.0
        implied_growth = None
        for _ in range(60):
            mid = (low + high) / 2
            pv = _dcf(mid)
            if abs(pv - market_cap) < 1e-3:
                implied_growth = mid
                break
            if pv > market_cap:
                high = mid
            else:
                low = mid
        if implied_growth is None:
            implied_growth = mid
        reasonableness = "aggressive" if implied_growth > 0.15 else ("modest" if implied_growth > 0.05 else "conservative")

        return {
            "status": "success",
            "data": {
                "implied_growth_rate": implied_growth,
                "implied_growth_years": years,
                "reasonableness_check": reasonableness,
                "vs_historical_growth": "unknown"
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"reverse_dcf failed: {e}")
        _log_lesson(f"reverse_dcf: {e}")
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
