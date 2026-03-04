"""Generate a Python SDK for Snowdrop MCP."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import textwrap

from skills.utils import _log_lesson

TOOL_META: dict[str, Any] = {
    "name": "python_sdk_generator",
    "description": "Builds a basic Python client with typed methods for each Snowdrop skill.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "skills": {"type": "array", "items": {"type": "object"}},
            "server_url": {"type": "string"},
            "package_name": {"type": "string", "default": "snowdrop_client"},
        },
        "required": ["skills", "server_url"],
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


def python_sdk_generator(
    skills: list[dict[str, Any]],
    server_url: str,
    package_name: str = "snowdrop_client",
    **_: Any,
) -> dict[str, Any]:
    """Return Python SDK code string with typed client methods."""

    try:
        methods = []
        for meta in skills:
            name = meta.get("name")
            if not name:
                continue
            method = _build_method(name, meta.get("inputSchema", {}))
            methods.append(method)
        sdk_code = _build_module(package_name, server_url, methods)
        usage_example = (
            "from snowdrop_client import SnowdropClient\n"
            "client = SnowdropClient(api_key=\"sk-123\")\n"
            f"result = client.{skills[0]['name']}(**{{}}) if skills else None"
        )
        data = {
            "sdk_code": sdk_code,
            "filename": f"{package_name}.py",
            "methods_generated": len(methods),
            "usage_example": usage_example,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("python_sdk_generator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _build_module(package_name: str, server_url: str, methods: list[str]) -> str:
    """Construct the SDK module source."""

    header = textwrap.dedent(
        f'''"""Auto-generated Snowdrop SDK."""

import json
import time
from dataclasses import dataclass
from typing import Any, Dict

import requests


@dataclass
class SnowdropClient:
    api_key: str
    base_url: str = "{server_url}"
    timeout: int = 30

    def _request(self, endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        for attempt in range(3):
            response = requests.post(
                f"{server_url}{{endpoint}}",
                headers={{"Authorization": f"Bearer {{self.api_key}}", "Content-Type": "application/json"}},
                data=json.dumps(payload),
                timeout=self.timeout,
            )
            if response.ok:
                return response.json()
            time.sleep(2 ** attempt)
        response.raise_for_status()
'''
    )
    methods_block = "\n".join(methods)
    return header + ("\n" + methods_block if methods_block else "")


def _build_method(name: str, schema: dict[str, Any]) -> str:
    """Create a client method for a single skill."""

    props = schema.get("properties", {}) or {}
    required = set(schema.get("required", []) or [])
    annotations = {
        "number": "float",
        "integer": "int",
        "array": "list[Any]",
        "object": "dict[str, Any]",
        "boolean": "bool",
        "string": "str",
    }
    parameters: list[str] = []
    payload_lines = ["        payload: dict[str, Any] = {}"]
    for prop, definition in props.items():
        annotation = annotations.get(definition.get("type"), "Any")
        optional_hint = "" if prop in required else " | None"
        default = "" if prop in required else " = None"
        parameters.append(f"        {prop}: {annotation}{optional_hint}{default},")
        payload_lines.append(f"        if {prop} is not None:")
        payload_lines.append(f"            payload[\"{prop}\"] = {prop}")
    parameters.append("        **extra: Any,")
    payload_lines.extend(
        [
            "        for key, value in extra.items():",
            "            if value is not None:",
            "                payload[key] = value",
        ]
    )
    params_block = "\n".join(parameters)
    payload_block = "\n".join(payload_lines)
    method = f"""
    def {name}(
{params_block}
    ) -> dict[str, Any]:
        \"\"\"Invoke the `{name}` skill.\"\"\"
{payload_block}
        return self._request("/tools/{name}", payload)
"""
    return textwrap.dedent(method)
