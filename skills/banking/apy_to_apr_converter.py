"""Convert APY to APR given compounding frequency.

MCP Tool Name: apy_to_apr_converter
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "apy_to_apr_converter",
    "description": "Convert Annual Percentage Yield (APY) to Annual Percentage Rate (APR) given compounding frequency. APR = n * ((1 + APY)^(1/n) - 1).",
    "inputSchema": {
        "type": "object",
        "properties": {
            "apy": {
                "type": "number",
                "description": "Annual Percentage Yield as a decimal (e.g., 0.05 for 5%).",
            },
            "compounds_per_year": {
                "type": "integer",
                "description": "Number of compounding periods per year (default 12 for monthly).",
                "default": 12,
            },
        },
        "required": ["apy"],
    },
}


def apy_to_apr_converter(apy: float, compounds_per_year: int = 12) -> dict[str, Any]:
    """Convert APY to APR given compounding frequency."""
    try:
        if compounds_per_year <= 0:
            return {
                "status": "error",
                "data": {"error": "compounds_per_year must be a positive integer."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        if apy <= -1:
            return {
                "status": "error",
                "data": {"error": "APY must be greater than -1 (i.e., -100%)."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        apr = compounds_per_year * ((1 + apy) ** (1 / compounds_per_year) - 1)

        return {
            "status": "ok",
            "data": {
                "apy": apy,
                "apy_pct": round(apy * 100, 4),
                "compounds_per_year": compounds_per_year,
                "apr": round(apr, 8),
                "apr_pct": round(apr * 100, 4),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
