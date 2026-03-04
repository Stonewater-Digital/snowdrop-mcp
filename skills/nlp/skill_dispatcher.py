"""Dispatch intents and entities to the right Snowdrop skill."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "skill_dispatcher",
    "description": "Maps classified intents and extracted entities into MCP skill payloads.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "intent": {"type": "string"},
            "entities": {
                "type": "array",
                "items": {"type": "object"},
            },
            "skill_registry": {"type": "object"},
        },
        "required": ["intent", "entities", "skill_registry"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "skill_name": {"type": "string"},
                    "params": {"type": "object"},
                    "missing_params": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "ready": {"type": "boolean"},
                },
            },
            "timestamp": {"type": "string"},
        },
    },
}

SKILL_PARAM_RULES: dict[str, list[str]] = {
    "payment": ["amount", "to_address", "currency", "memo"],
    "reconcile": ["ledger_balances", "live_balances"],
    "balance": ["account_id"],
    "report": ["date_range"],
    "scenario": ["scenario_params"],
}

ENTITY_TO_PARAM = {
    "amount": "amount",
    "currency": "currency",
    "agent_id": "agent_id",
    "account": "account_id",
    "date": "date",
    "asset": "asset",
}


def skill_dispatcher(
    intent: str,
    entities: list[dict[str, Any]],
    skill_registry: dict[str, Any],
    **_: Any,
) -> dict[str, Any]:
    """Return the skill name, parameter map, and readiness state."""

    try:
        if not skill_registry:
            raise ValueError("skill_registry must include at least one entry")
        chosen_skill = _select_skill(intent, list(skill_registry))
        params = _entities_to_params(entities)
        expected_params = _expected_params(chosen_skill)
        missing = [name for name in expected_params if name not in params]
        ready = not missing
        data = {
            "skill_name": chosen_skill,
            "params": params,
            "missing_params": missing,
            "ready": ready,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("skill_dispatcher", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _select_skill(intent: str, skills: list[str]) -> str:
    if not intent:
        return skills[0]
    intent_lower = intent.lower()
    for skill in skills:
        if intent_lower in skill.lower():
            return skill
    for skill in skills:
        for keyword in SKILL_PARAM_RULES:
            if keyword in skill.lower() and keyword in intent_lower:
                return skill
    return skills[0]


def _entities_to_params(entities: list[dict[str, Any]]) -> dict[str, Any]:
    params: dict[str, Any] = {}
    for entity in entities:
        key = entity.get("type")
        value = entity.get("value")
        param_name = ENTITY_TO_PARAM.get(key)
        if param_name and param_name not in params:
            params[param_name] = value
    return params


def _expected_params(skill_name: str) -> list[str]:
    for keyword, fields in SKILL_PARAM_RULES.items():
        if keyword in skill_name.lower():
            return fields
    return []


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
