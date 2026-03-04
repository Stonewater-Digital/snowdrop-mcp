import logging
from skills.utils.time import get_iso_timestamp

logger = logging.getLogger("snowdrop.skills")


def log_lesson(message: str) -> None:
    """Append a timestamped error lesson to logs/lessons.md.

    Args:
        message: Human-readable description of what went wrong.
    """
    try:
        with open("logs/lessons.md", "a", encoding="utf-8") as handle:
            handle.write(f"- [{get_iso_timestamp()}] {message}\n")
    except Exception as e:
        logger.error(f"Failed to log lesson: {e}")
