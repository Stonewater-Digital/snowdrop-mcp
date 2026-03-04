"""Validate data against a JSON schema-like rule set.

MCP Tool Name: json_schema_validator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "json_schema_validator",
    "description": "Validate a data object against a JSON schema-like rule set. Checks required fields, types, min/max constraints, and enum values.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "data": {
                "type": "object",
                "description": "The data object to validate.",
            },
            "schema": {
                "type": "object",
                "description": "Schema definition with 'properties' (field rules), 'required' (list of required field names). Each property can have: type (string/number/integer/boolean/array/object), minimum, maximum, enum, minLength, maxLength.",
            },
        },
        "required": ["data", "schema"],
    },
}

_TYPE_MAP = {
    "string": str,
    "number": (int, float),
    "integer": int,
    "boolean": bool,
    "array": list,
    "object": dict,
}


def _validate_field(field_name: str, value: Any, rules: dict[str, Any]) -> list[str]:
    """Validate a single field against its rules."""
    errors: list[str] = []

    # Type check
    expected_type = rules.get("type")
    if expected_type and expected_type in _TYPE_MAP:
        py_type = _TYPE_MAP[expected_type]
        if not isinstance(value, py_type):
            # Allow int for number type
            if expected_type == "number" and isinstance(value, (int, float)):
                pass
            else:
                errors.append(f"'{field_name}': expected type '{expected_type}', got '{type(value).__name__}'.")

    # Numeric constraints
    if isinstance(value, (int, float)):
        if "minimum" in rules and value < rules["minimum"]:
            errors.append(f"'{field_name}': value {value} is below minimum {rules['minimum']}.")
        if "maximum" in rules and value > rules["maximum"]:
            errors.append(f"'{field_name}': value {value} is above maximum {rules['maximum']}.")

    # String constraints
    if isinstance(value, str):
        if "minLength" in rules and len(value) < rules["minLength"]:
            errors.append(f"'{field_name}': length {len(value)} is below minLength {rules['minLength']}.")
        if "maxLength" in rules and len(value) > rules["maxLength"]:
            errors.append(f"'{field_name}': length {len(value)} is above maxLength {rules['maxLength']}.")

    # Enum check
    if "enum" in rules and value not in rules["enum"]:
        errors.append(f"'{field_name}': value '{value}' not in enum {rules['enum']}.")

    # Array constraints
    if isinstance(value, list):
        if "minItems" in rules and len(value) < rules["minItems"]:
            errors.append(f"'{field_name}': array has {len(value)} items, minimum is {rules['minItems']}.")
        if "maxItems" in rules and len(value) > rules["maxItems"]:
            errors.append(f"'{field_name}': array has {len(value)} items, maximum is {rules['maxItems']}.")

    return errors


def json_schema_validator(
    data: dict[str, Any],
    schema: dict[str, Any],
) -> dict[str, Any]:
    """Validate data against JSON schema-like rules."""
    try:
        errors: list[str] = []
        warnings: list[str] = []

        # Check required fields
        required = schema.get("required", [])
        for field in required:
            if field not in data:
                errors.append(f"Missing required field: '{field}'.")

        # Validate each property defined in schema
        properties = schema.get("properties", {})
        for field_name, rules in properties.items():
            if field_name in data:
                field_errors = _validate_field(field_name, data[field_name], rules)
                errors.extend(field_errors)

        # Check for extra fields not in schema
        if properties:
            extra = set(data.keys()) - set(properties.keys())
            if extra:
                warnings.append(f"Extra fields not in schema: {sorted(extra)}")

        is_valid = len(errors) == 0

        return {
            "status": "ok",
            "data": {
                "valid": is_valid,
                "errors": errors,
                "warnings": warnings,
                "fields_checked": len(properties),
                "required_fields": required,
                "data_fields": sorted(data.keys()),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
