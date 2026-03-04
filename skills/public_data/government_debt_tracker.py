"""Track total US public debt from the Treasury Fiscal Data API.

MCP Tool Name: government_debt_tracker
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "government_debt_tracker",
    "description": "Fetch total US public debt outstanding from the Treasury Fiscal Data API (Debt to the Penny). No API key required.",
    "inputSchema": {
        "type": "object",
        "properties": {},
        "required": [],
    },
}


def government_debt_tracker() -> dict[str, Any]:
    """Fetch total US public debt outstanding."""
    try:
        import httpx

        url = "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v2/accounting/od/debt_to_penny"
        params = {
            "sort": "-record_date",
            "page[size]": "1",
        }

        with httpx.Client(timeout=30) as client:
            resp = client.get(url, params=params)
            resp.raise_for_status()
            data = resp.json()

        records = data.get("data", [])
        if not records:
            return {
                "status": "error",
                "data": {"error": "No debt data returned from API."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        record = records[0]
        total_debt = float(record.get("tot_pub_debt_out_amt", 0))
        debt_held_public = float(record.get("debt_held_public_amt", 0))
        intragov = float(record.get("intragov_hold_amt", 0))

        return {
            "status": "ok",
            "data": {
                "record_date": record.get("record_date"),
                "total_public_debt_outstanding": total_debt,
                "total_public_debt_formatted": f"${total_debt:,.2f}",
                "debt_held_by_public": debt_held_public,
                "intragovernmental_holdings": intragov,
                "description": "Total Public Debt Outstanding (Debt to the Penny), US Treasury.",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
