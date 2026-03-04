"""Convert APR to APY given compounding frequency.

MCP Tool Name: apr_to_apy_converter
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "apr_to_apy_converter",
    "description": "Convert Annual Percentage Rate (APR) to Annual Percentage Yield (APY) given compounding frequency. APY = (1 + APR/n)^n - 1.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "apr": {
                "type": "number",
                "description": "Annual Percentage Rate as a decimal (e.g., 0.05 for 5%).",
            },
            "compounds_per_year": {
                "type": "integer",
                "description": "Number of compounding periods per year (default 12 for monthly).",
                "default": 12,
            },
        },
        "required": ["apr"],
    },
}


def apr_to_apy_converter(apr: float, compounds_per_year: int = 12) -> dict[str, Any]:
    """Convert APR to APY given compounding frequency."""
    try:
        if compounds_per_year <= 0:
            return {
                "status": "error",
                "data": {"error": "compounds_per_year must be a positive integer."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        apy = (1 + apr / compounds_per_year) ** compounds_per_year - 1

        return {
            "status": "ok",
            "data": {
                "apr": apr,
                "apr_pct": round(apr * 100, 4),
                "compounds_per_year": compounds_per_year,
                "apy": round(apy, 8),
                "apy_pct": round(apy * 100, 4),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
