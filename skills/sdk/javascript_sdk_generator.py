"""Generate a JavaScript Snowdrop client SDK."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "javascript_sdk_generator",
    "description": "Builds an ES module client with fetch wrappers and TypeScript types for skills.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "skills": {"type": "array", "items": {"type": "object"}},
            "server_url": {"type": "string"},
            "package_name": {"type": "string", "default": "snowdrop-client"},
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


def javascript_sdk_generator(
    skills: list[dict[str, Any]],
    server_url: str,
    package_name: str = "snowdrop-client",
    **_: Any,
) -> dict[str, Any]:
    """Return JS client and type definition strings."""
    try:
        methods = []
        types = ["export interface SnowdropResponse { status: string; data: any; timestamp: string; }"]
        for meta in skills:
            name = meta.get("name")
            if not name:
                continue
            methods.append(_build_js_method(name))
            types.append(_build_ts_type(name, meta.get("inputSchema", {})))
        sdk_code = _build_js_client(server_url, methods)
        types_code = "\n".join(types)
        usage_example = (
            "import { SnowdropClient } from './snowdrop-client.js';\n"
            "const client = new SnowdropClient('sk-123');\n"
            f"const result = await client.{skills[0]['name']}({{}});" if skills else ""
        )
        data = {
            "sdk_code": sdk_code,
            "types_code": types_code,
            "filename": f"{package_name}.js",
            "usage_example": usage_example,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("javascript_sdk_generator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _build_js_client(server_url: str, methods: list[str]) -> str:
    header = f"""export class SnowdropClient {{\n  constructor(apiKey, baseUrl = '{server_url}') {{\n    this.apiKey = apiKey;\n    this.baseUrl = baseUrl;\n  }}\n\n  async _request(path, body) {{\n    const response = await fetch(`${{this.baseUrl}}${{path}}`, {{\n      method: 'POST',\n      headers: {{\n        'Authorization': `Bearer ${{this.apiKey}}`,\n        'Content-Type': 'application/json'\n      }},\n      body: JSON.stringify(body)\n    }});\n    if (!response.ok) throw new Error(`Snowdrop error: ${{response.status}}`);\n    return await response.json();\n  }}\n"""
    return header + "\n".join(methods) + "}\n"


def _build_js_method(name: str) -> str:
    return (
        f"\n  async {name}(payload) {{\n    return await this._request('/tools/{name}', payload);\n  }}\n"
    )


def _build_ts_type(name: str, schema: dict[str, Any]) -> str:
    props = schema.get("properties", {}) or {}
    lines = [f"export interface {name.title()}Input {{"]
    for prop, definition in props.items():
        ts_type = "any"
        dtype = definition.get("type")
        if dtype == "number":
            ts_type = "number"
        elif dtype == "integer":
            ts_type = "number"
        elif dtype == "object":
            ts_type = "Record<string, any>"
        elif dtype == "array":
            ts_type = "any[]"
        else:
            ts_type = "string"
        optional = "?" if prop not in (schema.get("required", []) or []) else ""
        lines.append(f"  {prop}{optional}: {ts_type};")
    lines.append("}")
    return "\n".join(lines)


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
