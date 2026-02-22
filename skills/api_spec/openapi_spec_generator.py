"""Generate OpenAPI specification from TOOL_META definitions."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "openapi_spec_generator",
    "description": "Converts Snowdrop skill metadata into an OpenAPI 3.0.3 specification.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "skills": {
                "type": "array",
                "items": {"type": "object"},
            },
            "server_url": {"type": "string", "default": "https://snowdrop.fly.dev"},
            "api_version": {"type": "string", "default": "1.0.0"},
        },
        "required": ["skills"],
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


def openapi_spec_generator(
    skills: list[dict[str, Any]],
    server_url: str = "https://snowdrop.fly.dev",
    api_version: str = "1.0.0",
    **_: Any,
) -> dict[str, Any]:
    """Return an OpenAPI spec covering the provided skills."""
    try:
        if not skills:
            raise ValueError("skills list cannot be empty")
        paths: dict[str, Any] = {}
        for meta in skills:
            name = meta.get("name")
            if not name:
                raise ValueError("Each skill must include a name")
            path = f"/tools/{name}"
            input_schema = meta.get("inputSchema", {}) or {}
            output_schema = meta.get("outputSchema", {}) or {}
            paths[path] = {
                "post": {
                    "summary": meta.get("description", ""),
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": input_schema,
                            }
                        },
                    },
                    "responses": {
                        "200": {
                            "description": "Successful execution",
                            "content": {
                                "application/json": {
                                    "schema": output_schema,
                                }
                            },
                        }
                    },
                }
            }

        spec = {
            "openapi": "3.0.3",
            "info": {
                "title": "Snowdrop Tools API",
                "version": api_version,
                "description": "OpenAPI wrapper exposing Snowdrop skills.",
            },
            "servers": [{"url": server_url}],
            "paths": paths,
            "components": {
                "securitySchemes": {
                    "ApiKeyAuth": {
                        "type": "apiKey",
                        "in": "header",
                        "name": "X-Snowdrop-Key",
                    }
                }
            },
            "security": [{"ApiKeyAuth": []}],
        }
        return {
            "status": "success",
            "data": {"openapi_spec": spec},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("openapi_spec_generator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
