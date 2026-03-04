"""
Execuve Summary: Calculates the PEG ratio and interprets valuation versus growth.
Inputs: pe_ratio (float), earnings_growth_rate (float), dividend_yield (float|None)
Outputs: peg_ratio (float), interpretation (str), peter_lynch_threshold (str), peg_adjusted_for_yield (float|None)
MCP Tool Name: peg_ratio_calculator
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "peg_ratio_calculator",
    "description": "Evaluates PEG ratio relative to growth and adjusts for dividend yield when provided.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "pe_ratio": {"type": "number", "description": "Price-to-earnings ratio."},
            "earnings_growth_rate": {"type": "number", "description": "Expected EPS growth (decimal)."},
            "dividend_yield": {"type": "number", "description": "Optional dividend yield (decimal)."}
        },
        "required": ["pe_ratio", "earnings_growth_rate"]
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "timestamp": {"type": "string"}, "data": {"type": "object"}}, "required": ["status", "timestamp"]
    }
}


def peg_ratio_calculator(**kwargs: Any) -> dict:
    """Computes PEG and an adjusted PEG including dividend yield."""
    try:
        pe = kwargs.get("pe_ratio")
        growth = kwargs.get("earnings_growth_rate")
        dividend_yield = kwargs.get("dividend_yield")
        for label, value in (("pe_ratio", pe), ("earnings_growth_rate", growth)):
            if not isinstance(value, (int, float)):
                raise ValueError(f"{label} must be numeric")
        if growth <= 0:
            raise ValueError("earnings_growth_rate must be positive")

        peg_ratio = pe / (growth * 100)
        interpretation = "undervalued" if peg_ratio < 1 else ("fair" if peg_ratio <= 2 else "overvalued")
        peter_lynch_threshold = "attractive" if peg_ratio <= 1 else "caution"
        peg_adjusted = None
        if isinstance(dividend_yield, (int, float)) and dividend_yield >= 0:
            peg_adjusted = pe / ((growth + dividend_yield) * 100)

        return {
            "status": "success",
            "data": {
                "peg_ratio": peg_ratio,
                "interpretation": interpretation,
                "peter_lynch_threshold": peter_lynch_threshold,
                "peg_adjusted_for_yield": peg_adjusted
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"peg_ratio_calculator failed: {e}")
        _log_lesson(f"peg_ratio_calculator: {e}")
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
