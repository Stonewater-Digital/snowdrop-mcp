"""Shared helper that matches legacy `_log_lesson` signature."""

from __future__ import annotations

from skills.utils.logging import log_lesson


def _log_lesson(skill_name: str, error: str) -> None:
    """Proxy to the shared lesson logger with consistent formatting."""

    log_lesson(f"{skill_name}: {error}")

