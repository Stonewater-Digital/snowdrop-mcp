"""Coordinate the Haiku→Sonnet→Opus assembly line."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

CONFIG_PATH = Path("config/config.yaml")
MODEL_RATE_PER_1K = {
    "draft": 0.20,  # Haiku
    "default": 1.60,  # Sonnet
    "certification": 4.00,  # Opus
}

TOOL_META: dict[str, Any] = {
    "name": "assembly_line_orchestrator",
    "description": "Frames the Haiku→Sonnet→Opus workflow and estimates token spend.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "task_id": {"type": "string"},
            "brief": {"type": "string"},
            "estimated_tokens": {
                "type": "object",
                "description": "Estimated tokens per stage (haiku/sonnet/opus).",
            },
        },
        "required": ["task_id", "brief"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "task_plan": {"type": "array"},
                    "total_cost": {"type": "number"},
                    "config_hash": {"type": "string"},
                },
            },
            "timestamp": {"type": "string"},
        },
    },
}


def assembly_line_orchestrator(
    task_id: str,
    brief: str,
    estimated_tokens: dict[str, float] | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Build the Assembly Line execution plan."""
    try:
        config = _load_config()
        pipeline = config.get("assembly_line", {}).get("pipeline", [])
        if not pipeline:
            raise ValueError("assembly_line.pipeline missing from config")

        token_estimates = {k.lower(): float(v) for k, v in (estimated_tokens or {}).items()}
        task_plan = []
        total_cost = 0.0
        for stage in pipeline:
            stage_name = stage.get("stage")
            model_key = stage.get("model")
            model_info = config.get("models", {}).get(model_key or "")
            if not stage_name or not model_key or not model_info:
                raise ValueError(f"Invalid stage definition: {stage}")
            tokens = token_estimates.get(stage_name.lower(), token_estimates.get(model_key, 0.0))
            rate = MODEL_RATE_PER_1K.get(model_key, 1.0)
            cost = (tokens / 1000.0) * rate
            total_cost += cost
            task_plan.append({
                "stage": stage_name,
                "model_key": model_key,
                "model_id": model_info.get("model_id"),
                "estimated_tokens": round(tokens, 0),
                "rate_per_1k": rate,
                "estimated_cost": round(cost, 4),
            })

        data = {
            "task_id": task_id,
            "brief": brief,
            "task_plan": task_plan,
            "total_cost": round(total_cost, 4),
            "config_hash": str(hash(json.dumps(config, sort_keys=True)))
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("assembly_line_orchestrator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _load_config() -> dict[str, Any]:
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"Config file not found: {CONFIG_PATH}")
    with CONFIG_PATH.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
