"""Check Solana balances via JSON-RPC."""
from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any

import requests

LAMPORTS_PER_SOL = 1_000_000_000

TOOL_META: dict[str, Any] = {
    "name": "sol_balance_checker",
    "description": "Calls Solana RPC getBalance and returns SOL for the configured wallet.",
    "inputSchema": {"type": "object", "properties": {}},
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "address": {"type": "string"},
                    "balance_sol": {"type": "number"},
                },
            },
            "timestamp": {"type": "string"},
        },
    },
}


def sol_balance_checker(**_: Any) -> dict[str, Any]:
    """Fetch SOL balance from RPC."""
    try:
        address = os.getenv("SOL_WALLET_ADDRESS")
        rpc_url = os.getenv("SOLANA_RPC_URL")
        if not address or not rpc_url:
            raise ValueError("SOL_WALLET_ADDRESS and SOLANA_RPC_URL required (.env.template)")

        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getBalance",
            "params": [address],
        }
        response = requests.post(rpc_url, json=payload, timeout=15)
        response.raise_for_status()
        result = response.json().get("result", {})
        lamports = int(result.get("value", 0))
        balance_sol = lamports / LAMPORTS_PER_SOL
        data = {
            "address": address,
            "balance_sol": round(balance_sol, 4),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("sol_balance_checker", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
