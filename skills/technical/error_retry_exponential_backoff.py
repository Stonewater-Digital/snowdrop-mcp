"""
Executive Summary: Generate exponential backoff retry schedules with optional jitter for production-grade error handling.
Inputs: operation_name (str), max_retries (int), base_delay_seconds (float), max_delay_seconds (float), jitter (bool)
Outputs: retry_schedule (list of dicts), total_max_wait (float), configuration (dict)
MCP Tool Name: error_retry_exponential_backoff
"""
import os
import math
import random
import logging
from typing import Any
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "error_retry_exponential_backoff",
    "description": "Generate an exponential backoff retry schedule with optional jitter for production error handling. Returns per-attempt delays and total max wait time.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "operation_name": {
                "type": "string",
                "description": "Human-readable name of the operation being retried (for logging)."
            },
            "max_retries": {
                "type": "integer",
                "description": "Maximum number of retry attempts (default 3).",
                "default": 3
            },
            "base_delay_seconds": {
                "type": "number",
                "description": "Initial delay before first retry in seconds (default 1.0).",
                "default": 1.0
            },
            "max_delay_seconds": {
                "type": "number",
                "description": "Maximum cap on any single retry delay in seconds (default 60.0).",
                "default": 60.0
            },
            "jitter": {
                "type": "boolean",
                "description": "Whether to add random jitter to prevent thundering herd (default true).",
                "default": True
            }
        },
        "required": ["operation_name"]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "retry_schedule": {
                "type": "array",
                "items": {"type": "object"},
                "description": "Per-attempt schedule with delay and cumulative wait."
            },
            "total_max_wait": {
                "type": "number",
                "description": "Maximum total wait time across all retries in seconds."
            },
            "configuration": {"type": "object"},
            "status": {"type": "string"},
            "timestamp": {"type": "string"}
        },
        "required": ["retry_schedule", "total_max_wait", "configuration", "status", "timestamp"]
    }
}


def _compute_delay(
    attempt: int,
    base_delay: float,
    max_delay: float,
    jitter: bool,
    rng: random.Random,
) -> float:
    """Compute the delay for a given retry attempt.

    Formula: delay = min(base * 2^attempt, max_delay)
    With jitter: delay = uniform(0, delay)  (full jitter strategy)

    Full jitter is preferred over additive jitter for distributed systems
    because it spreads retries across the full window, minimizing collision
    probability in fan-out scenarios.

    Args:
        attempt: Zero-indexed attempt number (0 = first retry).
        base_delay: Base delay in seconds.
        max_delay: Maximum delay cap in seconds.
        jitter: Whether to apply full jitter.
        rng: Random number generator for reproducibility in tests.

    Returns:
        Computed delay in seconds, rounded to 3 decimal places.
    """
    exponential = min(base_delay * (2 ** attempt), max_delay)
    if jitter:
        delay = rng.uniform(0.0, exponential)
    else:
        delay = exponential
    return round(delay, 3)


def error_retry_exponential_backoff(
    operation_name: str,
    max_retries: int = 3,
    base_delay_seconds: float = 1.0,
    max_delay_seconds: float = 60.0,
    jitter: bool = True,
) -> dict:
    """Generate an exponential backoff retry schedule for a named operation.

    Uses the "full jitter" strategy (uniform(0, cap)) when jitter=True, which
    provides superior thundering-herd prevention compared to additive jitter.
    The worst-case total wait (no jitter) equals sum of all capped exponential
    delays. With jitter the expected wait is approximately half that value.

    Args:
        operation_name: Human-readable name of the operation (used in labels).
        max_retries: Total number of retry attempts (not counting initial try).
        base_delay_seconds: Initial delay before first retry in seconds.
        max_delay_seconds: Maximum cap for any single delay in seconds.
        jitter: If True, apply full jitter to all delays.

    Returns:
        A dict with keys:
            - retry_schedule (list): Per-attempt dicts with attempt number, delay_seconds,
              cumulative_wait_seconds, and exponential_cap_seconds.
            - total_max_wait (float): Worst-case total wait (no jitter) in seconds.
            - configuration (dict): Echo of all input parameters.
            - status (str): "success" or "error".
            - timestamp (str): ISO 8601 UTC timestamp.
    """
    try:
        if not operation_name:
            raise ValueError("operation_name cannot be empty.")
        if max_retries < 0:
            raise ValueError(f"max_retries must be >= 0, got {max_retries}.")
        if max_retries > 100:
            raise ValueError(f"max_retries capped at 100, got {max_retries}.")
        if base_delay_seconds <= 0:
            raise ValueError(f"base_delay_seconds must be positive, got {base_delay_seconds}.")
        if max_delay_seconds <= 0:
            raise ValueError(f"max_delay_seconds must be positive, got {max_delay_seconds}.")
        if max_delay_seconds < base_delay_seconds:
            raise ValueError(
                f"max_delay_seconds ({max_delay_seconds}) must be >= base_delay_seconds ({base_delay_seconds})."
            )

        # Use a seeded RNG for deterministic jitter in the schedule preview
        # (in real usage the caller would sample from this distribution each attempt)
        rng = random.Random(42)

        retry_schedule: list[dict] = []
        cumulative_wait = 0.0

        for attempt in range(max_retries):
            # Exponential cap (no jitter) for worst-case analysis
            exponential_cap = round(min(base_delay_seconds * (2 ** attempt), max_delay_seconds), 3)

            # Sampled delay (with or without jitter)
            sampled_delay = _compute_delay(
                attempt, base_delay_seconds, max_delay_seconds, jitter, rng
            )
            cumulative_wait += sampled_delay

            retry_schedule.append({
                "attempt": attempt + 1,
                "delay_seconds": sampled_delay,
                "exponential_cap_seconds": exponential_cap,
                "cumulative_wait_seconds": round(cumulative_wait, 3),
                "label": f"{operation_name} retry {attempt + 1}/{max_retries}",
                "jitter_applied": jitter,
            })

        # Total max wait = sum of all exponential caps (worst case, no jitter)
        total_max_wait = round(
            sum(min(base_delay_seconds * (2 ** i), max_delay_seconds) for i in range(max_retries)), 3
        )

        # Expected total wait with full jitter = half of total_max_wait (approx)
        expected_total_wait_with_jitter = round(total_max_wait / 2.0, 3) if jitter else total_max_wait

        configuration = {
            "operation_name": operation_name,
            "max_retries": max_retries,
            "base_delay_seconds": base_delay_seconds,
            "max_delay_seconds": max_delay_seconds,
            "jitter": jitter,
            "jitter_strategy": "full_jitter (uniform 0..cap)" if jitter else "none",
            "backoff_formula": "min(base * 2^attempt, max_delay)",
            "total_max_wait_seconds": total_max_wait,
            "expected_total_wait_seconds": expected_total_wait_with_jitter,
        }

        return {
            "status": "success",
            "retry_schedule": retry_schedule,
            "total_max_wait": total_max_wait,
            "expected_total_wait": expected_total_wait_with_jitter,
            "configuration": configuration,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        logger.error(f"error_retry_exponential_backoff failed: {e}")
        _log_lesson(f"error_retry_exponential_backoff: {e}")
        return {
            "status": "error",
            "error": str(e),
            "retry_schedule": [],
            "total_max_wait": 0.0,
            "configuration": {},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(message: str) -> None:
    """Append an error lesson to the lessons log file.

    Args:
        message: The lesson message to record.
    """
    try:
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        logger.warning("Could not write to logs/lessons.md")
