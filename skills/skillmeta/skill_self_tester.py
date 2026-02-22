"""Smoke test Snowdrop skills by introspecting TOOL_META."""
from __future__ import annotations

import importlib.util
import os
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "skill_self_tester",
    "description": "Generates test payloads from TOOL_META.inputSchema and runs the skill function.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "skill_module_path": {"type": "string"},
            "num_tests": {"type": "integer", "default": 3},
        },
        "required": ["skill_module_path"],
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


def skill_self_tester(
    skill_module_path: str,
    num_tests: int = 3,
    **_: Any,
) -> dict[str, Any]:
    """Run generated tests against a skill module."""
    try:
        module = _load_module(skill_module_path)
        tool_meta = getattr(module, "TOOL_META", None)
        if not tool_meta:
            raise ValueError("Skill module missing TOOL_META")
        func_name = os.path.splitext(os.path.basename(skill_module_path))[0]
        skill_func = getattr(module, func_name)
        schema = tool_meta.get("inputSchema", {})
        required_fields = schema.get("required", [])
        properties = schema.get("properties", {})
        passed = 0
        failed = 0
        errors: list[dict[str, Any]] = []
        for idx in range(num_tests):
            payload = {
                field: _sample_value(properties.get(field, {}), idx)
                for field in required_fields
            }
            try:
                result = skill_func(**payload)
                if result.get("status") == "success":
                    passed += 1
                else:
                    failed += 1
                    errors.append({"test": idx + 1, "error": result})
            except Exception as err:
                failed += 1
                errors.append({"test": idx + 1, "error": str(err)})
        coverage = f"required_fields:{len(required_fields)} tests:{num_tests}"
        data = {
            "passed": passed,
            "failed": failed,
            "errors": errors,
            "coverage": coverage,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("skill_self_tester", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _load_module(path: str):
    if not os.path.exists(path):
        raise ValueError("skill_module_path not found")
    spec = importlib.util.spec_from_file_location("skill_self_test_target", path)
    module = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
    assert spec and spec.loader
    spec.loader.exec_module(module)  # type: ignore[attr-defined]
    return module


def _sample_value(schema: dict[str, Any], seed: int) -> Any:
    schema_type = schema.get("type", "string")
    if isinstance(schema_type, list):
        schema_type = schema_type[0]
    if schema_type == "string":
        return schema.get("default", f"test-{seed}")
    if schema_type == "number":
        return schema.get("default", 1.0)
    if schema_type == "integer":
        return int(schema.get("default", 1))
    if schema_type == "boolean":
        return bool(schema.get("default", True))
    if schema_type == "array":
        item_schema = schema.get("items", {"type": "string"})
        return [_sample_value(item_schema, seed)]
    if schema_type == "object":
        props = schema.get("properties", {})
        req = schema.get("required", props.keys())
        return {key: _sample_value(props.get(key, {}), seed) for key in req}
    return schema.get("default", f"test-{seed}")


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
