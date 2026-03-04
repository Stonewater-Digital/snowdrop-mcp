"""Fetch average interest rates for Treasury securities from the US Treasury Fiscal Data API.

MCP Tool Name: treasury_yield_fetcher
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "treasury_yield_fetcher",
    "description": "Fetch average interest rates for US Treasury securities from the Fiscal Data API. No API key required.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "security_type": {
                "type": "string",
                "description": "Security description filter (e.g., 'Treasury Bills', 'Treasury Notes', 'Treasury Bonds').",
                "default": "Treasury Bills",
            },
            "days": {
                "type": "integer",
                "description": "Number of recent records to return.",
                "default": 30,
            },
        },
        "required": [],
    },
}


def treasury_yield_fetcher(
    security_type: str = "Treasury Bills",
    days: int = 30,
) -> dict[str, Any]:
    """Fetch average interest rates for US Treasury securities."""
    try:
        import httpx

        url = "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v2/accounting/od/avg_interest_rates"
        params = {
            "filter": f"security_desc:eq:{security_type}",
            "sort": "-record_date",
            "page[size]": str(days),
        }

        with httpx.Client(timeout=30) as client:
            resp = client.get(url, params=params)
            resp.raise_for_status()
            data = resp.json()

        records = data.get("data", [])
        clean = [
            {
                "date": r["record_date"],
                "security": r.get("security_desc", ""),
                "avg_interest_rate": float(r["avg_interest_rate_amt"]) if r.get("avg_interest_rate_amt") else None,
            }
            for r in records
        ]

        return {
            "status": "ok",
            "data": {
                "security_type": security_type,
                "count": len(clean),
                "records": clean,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
