"""Telemetry helpers for Snowdrop skills."""
from __future__ import annotations

import json
from pathlib import Path
from time import perf_counter
from typing import Any

from skills.utils.logging import logger
from skills.utils.time import get_iso_timestamp

TELEMETRY_LOG_PATH = Path("logs/skill_telemetry.jsonl")


def emit_skill_telemetry(sample: dict[str, Any], log_path: Path | None = None) -> None:
    """Write a telemetry sample to disk.

    Args:
        sample: Dictionary containing telemetry details.
        log_path: Optional override for the log destination.
    """
    log_file = log_path or TELEMETRY_LOG_PATH
    try:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        with log_file.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(_sanitize_sample(sample)) + "\n")
    except Exception as exc:  # noqa: BLE001
        logger.warning(f"emit_skill_telemetry failed: {exc}")


class SkillTelemetryEmitter:
    """Helper for recording latency + metadata telemetry."""

    def __init__(
        self,
        skill_name: str,
        base_metadata: dict[str, Any] | None = None,
        *,
        log_path: Path | None = None,
    ) -> None:
        self.skill_name = skill_name
        self.base_metadata = base_metadata or {}
        self._log_path = log_path
        self._start = perf_counter()

    def record(self, status: str, metadata: dict[str, Any] | None = None) -> None:
        """Record telemetry for the wrapped skill."""
        latency_ms = (perf_counter() - self._start) * 1000
        combined_metadata = {**self.base_metadata, **(metadata or {})}
        sample = {
            "skill_name": self.skill_name,
            "status": status,
            "latency_ms": round(latency_ms, 2),
            "timestamp": get_iso_timestamp(),
            "metadata": combined_metadata,
        }
        emit_skill_telemetry(sample, log_path=self._log_path)


def _sanitize_sample(sample: dict[str, Any]) -> dict[str, Any]:
    """Ensure telemetry sample is JSON serializable."""
    sanitized: dict[str, Any] = {}
    for key, value in sample.items():
        sanitized[key] = _to_primitive(value)
    return sanitized


def _to_primitive(value: Any) -> Any:
    """Convert nested structures to JSON-safe primitives."""
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    if isinstance(value, dict):
        return {str(k): _to_primitive(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_to_primitive(item) for item in value]
    return str(value)
