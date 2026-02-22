"""Generic ETL data transformer."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "data_transformer",
    "description": "Applies rename/cast/compute/drop/default transformations to dataset rows sequentially.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "data": {"type": "array", "items": {"type": "object"}},
            "transformations": {"type": "array", "items": {"type": "object"}},
        },
        "required": ["data", "transformations"],
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


def data_transformer(
    data: list[dict[str, Any]],
    transformations: list[dict[str, Any]],
    **_: Any,
) -> dict[str, Any]:
    """Return transformed dataset and audit log."""
    try:
        records = [row.copy() for row in data]
        log_entries: list[str] = []
        for transform in transformations:
            op = transform.get("operation")
            field = transform.get("field")
            if op == "rename":
                new_name = transform.get("params", {}).get("new_name")
                if not new_name:
                    raise ValueError("rename requires params.new_name")
                for row in records:
                    row[new_name] = row.pop(field, None)
                log_entries.append(f"rename {field} -> {new_name}")
            elif op == "cast":
                cast_type = transform.get("params", {}).get("type", "string")
                caster = _caster(cast_type)
                for row in records:
                    if field in row and row[field] is not None:
                        row[field] = caster(row[field])
                log_entries.append(f"cast {field} to {cast_type}")
            elif op == "compute":
                expression = transform.get("params", {}).get("expression")
                if not expression:
                    raise ValueError("compute requires params.expression")
                for row in records:
                    row[field] = _safe_eval(expression, row)
                log_entries.append(f"compute {field} = {expression}")
            elif op == "drop":
                for row in records:
                    row.pop(field, None)
                log_entries.append(f"drop {field}")
            elif op == "default":
                default_value = transform.get("params", {}).get("value")
                for row in records:
                    if row.get(field) in {None, ""}:
                        row[field] = default_value
                log_entries.append(f"default {field} -> {default_value}")
            else:
                raise ValueError(f"Unsupported operation: {op}")
        data_payload = {
            "records": records,
            "transformation_log": log_entries,
        }
        return {
            "status": "success",
            "data": data_payload,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("data_transformer", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _caster(name: str):
    mapping = {
        "string": str,
        "int": lambda value: int(float(value)),
        "float": float,
        "bool": lambda value: str(value).lower() in {"true", "1", "yes"},
    }
    if name not in mapping:
        raise ValueError(f"Unsupported cast type: {name}")
    return mapping[name]


def _safe_eval(expression: str, row: dict[str, Any]) -> Any:
    allowed = {key: value for key, value in row.items() if isinstance(key, str)}
    allowed["__builtins__"] = {}
    return eval(expression, allowed, {})


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
