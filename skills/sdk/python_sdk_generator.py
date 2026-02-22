"""Generate a Python SDK for Snowdrop MCP."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

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
    header = f""""""Auto-generated Snowdrop SDK."""\n\nimport json\nimport time\nfrom dataclasses import dataclass\nfrom typing import Any, Dict\n\nimport requests\n\n\n@dataclass\nclass SnowdropClient:\n    api_key: str\n    base_url: str = \"{server_url}\"\n    timeout: int = 30\n\n    def _request(self, endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:\n        for attempt in range(3):\n            response = requests.post(\n                f\"{server_url}{{endpoint}}\",\n                headers={{\"Authorization\": f\"Bearer {{self.api_key}}\", \"Content-Type\": \"application/json\"}},\n                data=json.dumps(payload),\n                timeout=self.timeout,\n            )\n            if response.ok:\n                return response.json()\n            time.sleep(2 ** attempt)\n        response.raise_for_status()\n"""
    return header + "\n".join(methods)


def _build_method(name: str, schema: dict[str, Any]) -> str:
    props = schema.get("properties", {}) or {}
    required = schema.get("required", []) or []
    parameters = []
    payload_lines = ["payload = {}"]
    for prop, definition in props.items():
        annotation = "Any"
        if definition.get("type") == "number":
            annotation = "float"
        elif definition.get("type") == "integer":
            annotation = "int"
        elif definition.get("type") == "array":
            annotation = "list"
        elif definition.get("type") == "object":
            annotation = "dict"
        else:
            annotation = "str"
        default = "" if prop in required else " = None"
        parameters.append(f"        {prop}: {annotation}{default}")
        payload_lines.append(f"        if {prop} is not None:\n            payload[\"{prop}\"] = {prop}")
    params_block = "\n".join(parameters) or "        **kwargs: Any"
    payload_block = "\n".join(payload_lines)
    method = f"""\n    def {name}(\n{params_block}\n    ) -> dict:\n        \"\"\"Invoke the `{name}` skill.\"\"\"\n{payload_block}\n        return self._request('/tools/{name}', payload)\n"""
    return method


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
