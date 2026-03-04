"""Track Snowdrop contracts end-to-end."""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "contract_lifecycle_manager",
    "description": "Creates, updates, lists, and surfaces contracts nearing expiration.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "operation": {
                "type": "string",
                "enum": ["create", "update", "list", "expiring"],
            },
            "contract": {"type": "object"},
            "lookahead_days": {"type": "integer", "default": 90},
        },
        "required": ["operation"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {"type": "object"},
            "timestamp": {"type": "string"},
        },
    },
}


_LOG_PATH = Path("logs/contracts.jsonl")


def contract_lifecycle_manager(
    operation: str,
    contract: dict[str, Any] | None = None,
    lookahead_days: int = 90,
    **_: Any,
) -> dict[str, Any]:
    """Manage contract lifecycle operations."""
    try:
        existing = _read_contracts()
        operation = operation.lower()
        if operation == "list":
            data = {"contracts": existing}
        elif operation == "create":
            if contract is None:
                raise ValueError("contract payload required for create")
            required = [
                "contract_id",
                "counterparty",
                "type",
                "value",
                "start_date",
                "end_date",
                "auto_renew",
            ]
            missing = [field for field in required if field not in contract]
            if missing:
                raise ValueError(f"Missing contract fields: {', '.join(missing)}")
            record = {**contract, "last_updated": datetime.now(timezone.utc).isoformat()}
            _append_contract(record)
            data = record
        elif operation == "update":
            if contract is None or "contract_id" not in contract:
                raise ValueError("contract_id required for update")
            merged = _merge_contract(existing, contract)
            _append_contract(merged)
            data = merged
        elif operation == "expiring":
            upcoming = _expiring_contracts(existing, lookahead_days)
            data = {"expiring": upcoming, "lookahead_days": lookahead_days}
        else:
            raise ValueError("Unsupported operation")

        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("contract_lifecycle_manager", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _read_contracts() -> list[dict[str, Any]]:
    if not _LOG_PATH.exists():
        return []
    records: list[dict[str, Any]] = []
    with _LOG_PATH.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return records


def _append_contract(record: dict[str, Any]) -> None:
    _LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with _LOG_PATH.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record) + "\n")


def _merge_contract(existing: list[dict[str, Any]], update: dict[str, Any]) -> dict[str, Any]:
    base = {}
    for record in reversed(existing):
        if record.get("contract_id") == update["contract_id"]:
            base = record.copy()
            break
    if not base:
        raise ValueError("Cannot update unknown contract_id")
    merged = {**base, **update, "last_updated": datetime.now(timezone.utc).isoformat()}
    return merged


def _expiring_contracts(records: list[dict[str, Any]], lookahead_days: int) -> list[dict[str, Any]]:
    window_end = datetime.now(timezone.utc).date() + timedelta(days=lookahead_days)
    today = datetime.now(timezone.utc).date()
    upcoming = []
    for contract in records:
        end_date_raw = contract.get("end_date")
        if not end_date_raw:
            continue
        try:
            end_date = datetime.fromisoformat(end_date_raw).date()
        except ValueError:
            continue
        days_remaining = (end_date - today).days
        if 0 <= days_remaining <= lookahead_days:
            upcoming.append({**contract, "days_remaining": days_remaining})
    upcoming.sort(key=lambda item: item["days_remaining"])
    return upcoming


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
