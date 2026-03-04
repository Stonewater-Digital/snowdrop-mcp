"""
llm_evaluator.py — LLM evaluation for the recruiting pipeline.

Executive Summary:
    Thin OpenRouter wrapper purpose-built for recruiting evaluation. Routes to
    scout (Gemini 2.5 Flash Lite), builder (Sonnet), or certify (Opus) tiers
    based on task_tier. Enforces budget checks and returns structured JSON.

MCP Tool Name: recruiting_llm_evaluator
"""
import json
import logging
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from openai import OpenAI

from config.models import resolve_model
from skills.utils.retry import retry

logger = logging.getLogger("snowdrop.recruiting_llm_evaluator")

TOOL_META: dict[str, Any] = {
    "name": "recruiting_llm_evaluator",
    "description": (
        "LLM evaluation for recruiting pipeline. Routes to scout/builder/certify tiers. "
        "Scout (Gemini 2.5 Flash Lite) does first-pass triage, builder (Sonnet) does "
        "substantive evaluation, certify (Opus) handles hire decisions only."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "prompt": {"type": "string", "description": "System prompt for the evaluation task."},
            "context": {"type": "string", "description": "The content to evaluate (candidate response, code, etc)."},
            "task_tier": {
                "type": "string",
                "enum": ["scout", "builder", "certify"],
                "description": "Evaluation tier: scout (cheap triage), builder (substantive), certify (hire decisions).",
            },
            "trace_id": {"type": "string", "description": "Correlation ID for traceability."},
            "response_format": {
                "type": "string",
                "enum": ["json", "text"],
                "default": "json",
            },
        },
        "required": ["prompt", "context", "task_tier", "trace_id"],
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

# Model IDs for each tier — resolved from config/config.yaml via resolve_model()
_TIER_MODELS: dict[str, str] = {
    "scout": "scout",
    "builder": "default",
    "certify": "certification",
}

_CONFIG_PATH = Path("config/config.yaml")


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _wrap(status: str, data: dict) -> dict:
    return {"status": status, "data": data, "timestamp": _now_iso()}


def _resolve_model(task_tier: str) -> str:
    """Resolve model ID from tier via central config/models.py."""
    if task_tier not in _TIER_MODELS:
        raise ValueError(f"Unknown task_tier '{task_tier}'. Use: scout, builder, certify")
    config_role = _TIER_MODELS[task_tier]
    return resolve_model(config_role)


def _check_budget() -> bool:
    """Check daily budget cap from config. Returns True if under budget."""
    try:
        import yaml
        if _CONFIG_PATH.exists():
            with _CONFIG_PATH.open("r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
            cap = config.get("budget", {}).get("daily_cap_usd", 50.0)
            if cap <= 0:
                return False
        return True
    except Exception as exc:
        logger.warning("Budget check failed, proceeding: %s", exc)
        return True


@retry(
    attempts=2,
    backoff_seconds=1.0,
    jitter=0.3,
    retriable_exceptions=(Exception,),
)
def _call_openrouter(model: str, system: str, user: str, response_format: str) -> str:
    """Call OpenRouter and return the response content."""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENROUTER_API_KEY not set")

    client = OpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=0.2,
    )
    content = response.choices[0].message.content
    if not content:
        raise RuntimeError(f"Empty response from model {model}")
    return content


def recruiting_llm_evaluator(
    prompt: str,
    context: str,
    task_tier: str,
    trace_id: str,
    response_format: str = "json",
) -> dict:
    """Evaluate recruiting content via LLM at the appropriate tier.

    Args:
        prompt: System prompt for the evaluation task.
        context: The content to evaluate (candidate response, code, etc).
        task_tier: "scout" | "builder" | "certify".
        trace_id: Correlation ID for traceability.
        response_format: "json" for structured output, "text" for free text.

    Returns:
        Standard Snowdrop envelope with LLM evaluation result.
    """
    logger.info("LLM eval: tier=%s trace_id=%s", task_tier, trace_id)

    try:
        model = _resolve_model(task_tier)

        if not _check_budget():
            return _wrap("error", {"error": "Daily budget cap exceeded", "trace_id": trace_id})

        json_instruction = ""
        if response_format == "json":
            json_instruction = "\n\nYou MUST respond with valid JSON only. No markdown, no explanation."

        raw = _call_openrouter(
            model=model,
            system=prompt + json_instruction,
            user=context,
            response_format=response_format,
        )

        # Parse JSON if requested
        evaluation: Any
        if response_format == "json":
            # Strip markdown fences if present
            cleaned = raw.strip()
            if cleaned.startswith("```"):
                lines = cleaned.split("\n")
                lines = [l for l in lines if not l.strip().startswith("```")]
                cleaned = "\n".join(lines)
            try:
                evaluation = json.loads(cleaned)
            except json.JSONDecodeError:
                logger.warning("Failed to parse JSON response, returning raw text: trace_id=%s", trace_id)
                evaluation = {"raw_text": raw, "parse_failed": True}
        else:
            evaluation = {"text": raw}

        result = {
            "trace_id": trace_id,
            "task_tier": task_tier,
            "model": model,
            "evaluation": evaluation,
        }

        logger.info("LLM eval complete: tier=%s model=%s trace_id=%s", task_tier, model, trace_id)
        return _wrap("ok", result)

    except EnvironmentError as exc:
        logger.error("Config error: %s", exc)
        return _wrap("error", {"error": str(exc), "trace_id": trace_id})
    except Exception as exc:
        logger.error("LLM eval error: %s", exc, exc_info=True)
        return _wrap("error", {"error": str(exc), "trace_id": trace_id})
