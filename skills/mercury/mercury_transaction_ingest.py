"""Ingest Mercury transactions for Ghost Ledger."""
from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any

import requests

API_BASE = "https://api.mercury.com/api/v1"

TOOL_META: dict[str, Any] = {
    "name": "mercury_transaction_ingest",
    "description": "Pulls Mercury transactions, tags inflow/outflow, and formats for Ghost Ledger.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "start_date": {"type": "string"},
            "end_date": {"type": "string"},
            "limit": {"type": "number"},
        },
        "required": ["start_date", "end_date"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "transactions": {"type": "array"},
                    "inflow_total": {"type": "number"},
                    "outflow_total": {"type": "number"},
                },
            },
            "timestamp": {"type": "string"},
        },
    },
}


def mercury_transaction_ingest(
    start_date: str,
    end_date: str,
    limit: int | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Fetch and normalize Mercury transactions."""
    try:
        token = os.getenv("MERCURY_API_TOKEN")
        if not token:
            raise ValueError("MERCURY_API_TOKEN missing; see .env.template")

        headers = {"Authorization": f"Bearer {token}"}
        params: dict[str, Any] = {"start": start_date, "end": end_date}
        if limit:
            params["limit"] = limit
        response = requests.get(
            f"{API_BASE}/transactions",
            headers=headers,
            params=params,
            timeout=20,
        )
        response.raise_for_status()
        payload = response.json()
        transactions = payload.get("transactions", payload.get("data", []))

        inflow_total = 0.0
        outflow_total = 0.0
        normalized = []
        for tx in transactions:
            amount = float(tx.get("amount", 0.0))
            direction = "inflow" if amount >= 0 else "outflow"
            if direction == "inflow":
                inflow_total += amount
            else:
                outflow_total += abs(amount)
            normalized.append({
                "id": tx.get("id"),
                "date": tx.get("date"),
                "counterparty": tx.get("counterparty", {}).get("name"),
                "memo": tx.get("memo"),
                "amount": round(amount, 2),
                "direction": direction,
                "ghost_ledger_tab": "THE WATERING HOLE" if amount >= 0 else "THE VAULT",
            })

        data = {
            "transactions": normalized,
            "inflow_total": round(inflow_total, 2),
            "outflow_total": round(outflow_total, 2),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("mercury_transaction_ingest", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
