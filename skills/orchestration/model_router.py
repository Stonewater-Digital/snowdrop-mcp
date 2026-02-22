"""Route tasks to the correct Snowdrop model."""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

CONFIG_PATH = Path("config/config.yaml")
CATEGORY_MAP = {
    "draft": "draft",
    "prototype": "draft",
    "build": "default",
    "finance": "default",
    "analysis": "default",
    "secretary": "secretary",
    "research": "secretary",
    "brief": "secretary",
    "skeptic": "skeptic",
    "audit": "skeptic",
    "jury": "certification",
    "charter": "certification",
    "certify": "certification",
}

TOOL_META: dict[str, Any] = {
    "name": "model_router",
    "description": "Reads config/config.yaml and maps a task category to the correct model entry.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "task_category": {"type": "string"},
            "urgency": {
                "type": "string",
                "description": "Optional urgency: low/standard/high",
            },
            "fallback_allowed": {"type": "boolean"},
        },
        "required": ["task_category"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "model_key": {"type": "string"},
                    "model_id": {"type": "string"},
                    "provider": {"type": "string"},
                    "reason": {"type": "string"},
                },
            },
            "timestamp": {"type": "string"},
        },
    },
}


def model_router(
    task_category: str,
    urgency: str | None = None,
    fallback_allowed: bool = True,
    **_: Any,
) -> dict[str, Any]:
    """Map task categories to configured models."""
    try:
        config = _load_config()
        models = config.get("models", {})
        normalized = task_category.lower().strip()
        model_key = CATEGORY_MAP.get(normalized)

        reason_parts = [f"category={normalized}"]
        if urgency:
            reason_parts.append(f"urgency={urgency}")

        if not model_key:
            reason_parts.append("category_not_mapped")
            model_key = "default" if fallback_allowed else None

        if not model_key or model_key not in models:
            raise ValueError(f"No model configured for category '{task_category}'")

        model_info = models[model_key]
        data = {
            "model_key": model_key,
            "model_id": model_info.get("model_id"),
            "provider": model_info.get("provider"),
            "via": model_info.get("via"),
            "reason": "; ".join(reason_parts),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("model_router", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _load_config() -> dict[str, Any]:
    if not CONFIG_PATH.exists():
        raise FileNotFoundError("config/config.yaml missing")
    with CONFIG_PATH.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
