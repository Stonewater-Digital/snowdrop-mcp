"""Validate data against lightweight JSON Schema."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "schema_validator",
    "description": "Checks arbitrary data payloads against JSON Schema definitions (subset).",
    "inputSchema": {
        "type": "object",
        "properties": {
            "data": {},
            "schema": {"type": "object"},
        },
        "required": ["data", "schema"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "valid": {"type": "boolean"},
                    "errors": {"type": "array", "items": {"type": "object"}},
                },
            },
            "timestamp": {"type": "string"},
        },
    },
}


def schema_validator(data: Any, schema: dict[str, Any], **_: Any) -> dict[str, Any]:
    """Return schema compliance result."""

    try:
        errors: list[dict[str, str]] = []
        _validate(data, schema, "root", errors)
        data_payload = {"valid": not errors, "errors": errors}
        return {
            "status": "success",
            "data": data_payload,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("schema_validator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _validate(value: Any, schema: dict[str, Any], path: str, errors: list[dict[str, str]]) -> None:
    schema_type = schema.get("type")
    if schema_type:
        if schema_type == "object" and not isinstance(value, dict):
            errors.append(_err(path, "object", type(value).__name__))
            return
        if schema_type == "array" and not isinstance(value, list):
            errors.append(_err(path, "array", type(value).__name__))
            return
        if schema_type == "string" and not isinstance(value, str):
            errors.append(_err(path, "string", type(value).__name__))
            return
        if schema_type == "number" and not isinstance(value, (int, float)):
            errors.append(_err(path, "number", type(value).__name__))
            return

    if schema_type == "object":
        required = schema.get("required", [])
        for field in required:
            if field not in value:
                errors.append({"path": f"{path}.{field}", "expected": "present", "actual": "missing", "message": "Field required"})
        properties = schema.get("properties", {})
        for key, subschema in properties.items():
            if key in value:
                _validate(value[key], subschema, f"{path}.{key}", errors)
    elif schema_type == "array":
        subschema = schema.get("items", {})
        for idx, item in enumerate(value):
            _validate(item, subschema, f"{path}[{idx}]", errors)
    else:
        if "enum" in schema and value not in schema["enum"]:
            errors.append({"path": path, "expected": f"enum {schema['enum']}", "actual": str(value), "message": "Value not allowed"})
        if "minimum" in schema and isinstance(value, (int, float)) and value < schema["minimum"]:
            errors.append({"path": path, "expected": f">={schema['minimum']}", "actual": str(value), "message": "Value below minimum"})


def _err(path: str, expected: str, actual: str) -> dict[str, str]:
    return {"path": path, "expected": expected, "actual": actual, "message": "Type mismatch"}


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
