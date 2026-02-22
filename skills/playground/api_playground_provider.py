"""Provide sandboxed sample runs for skills."""
from __future__ import annotations

import importlib
import random
import time
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "api_playground_provider",
    "description": "Generates sample inputs and sandboxed outputs for public skill demos.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "skill_name": {"type": "string"},
            "custom_input": {"type": ["object", "null"], "default": None},
            "use_sample": {"type": "boolean", "default": True},
        },
        "required": ["skill_name"],
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


def api_playground_provider(
    skill_name: str,
    custom_input: dict[str, Any] | None = None,
    use_sample: bool = True,
    **_: Any,
) -> dict[str, Any]:
    """Return sandbox preview data for a skill."""
    try:
        module = importlib.import_module(skill_name)
        meta = getattr(module, "TOOL_META", None)
        if not meta:
            raise ValueError("Skill TOOL_META not found")
        sample_input = custom_input if not use_sample else _build_sample(meta)
        start = time.perf_counter()
        # Sandbox: do not invoke live skill, return a placeholder output.
        output = {
            "note": "Sandbox preview only. Execute live via Watering Hole to run the skill.",
            "expected_schema": meta.get("outputSchema"),
        }
        latency_ms = int((time.perf_counter() - start) * 1000)
        data = {
            "input_used": sample_input,
            "output": output,
            "latency_ms": latency_ms,
            "sandbox": True,
            "try_live_cta": "Ready to go live? Use snowdrop invoke <skill> with your parameters.",
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("api_playground_provider", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _build_sample(meta: dict[str, Any]) -> dict[str, Any]:
    sample: dict[str, Any] = {}
    props = meta.get("inputSchema", {}).get("properties", {})
    for name, config in props.items():
        if "default" in config:
            sample[name] = config["default"]
        elif config.get("type") == "number":
            sample[name] = round(random.uniform(1, 100), 2)
        elif config.get("type") == "integer":
            sample[name] = random.randint(1, 10)
        elif config.get("type") == "boolean":
            sample[name] = True
        elif config.get("type") == "array":
            sample[name] = []
        else:
            sample[name] = f"sample_{name}"
    return sample


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
