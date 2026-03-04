"""
Executive Summary: IFRS 9 stage classification engine using PD migration, days past due, and qualitative SICR triggers.
Inputs: origination_pd (float), current_pd (float), sicr_threshold_pct (float), dpd_days (int), qualitative_triggers (list[str])
Outputs: stage (int), sicr_flag (bool), trigger_reason (str)
MCP Tool Name: ifrs9_stage_classifier
"""
import logging
from datetime import datetime, timezone
from typing import Any, List

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "ifrs9_stage_classifier",
    "description": "Classifies assets into IFRS 9 stages using PD migration and delinquency criteria.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "origination_pd": {"type": "number", "description": "PD at origination (decimal)."},
            "current_pd": {"type": "number", "description": "Current PD (decimal)."},
            "sicr_threshold_pct": {"type": "number", "description": "SICR threshold as % increase."},
            "dpd_days": {"type": "integer", "description": "Days past due."},
            "qualitative_triggers": {
                "type": "array",
                "description": "List of qualitative factors (e.g., watchlist).",
                "items": {"type": "string"},
            },
        },
        "required": ["origination_pd", "current_pd", "sicr_threshold_pct", "dpd_days", "qualitative_triggers"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "description": "status"},
            "data": {"type": "object", "description": "Stage output"},
            "timestamp": {"type": "string", "description": "timestamp"},
        },
        "required": ["status", "timestamp"],
    },
}


def ifrs9_stage_classifier(
    origination_pd: float,
    current_pd: float,
    sicr_threshold_pct: float,
    dpd_days: int,
    qualitative_triggers: List[str],
    **_: Any,
) -> dict[str, Any]:
    try:
        if origination_pd <= 0:
            raise ValueError("origination_pd must be positive")
        pd_change = (current_pd - origination_pd) / origination_pd
        sicr_flag = pd_change * 100 >= sicr_threshold_pct
        trigger_reason = ""
        stage = 1
        if dpd_days >= 90 or "default" in [trigger.lower() for trigger in qualitative_triggers]:
            stage = 3
            trigger_reason = "credit-impaired"
        elif dpd_days >= 30 or sicr_flag or qualitative_triggers:
            stage = 2
            trigger_reason = "sicr" if sicr_flag else "dpd" if dpd_days >= 30 else "qualitative"
        data = {
            "stage": stage,
            "sicr_flag": stage == 2,
            "pd_increase_pct": round(pd_change * 100, 2),
            "trigger_reason": trigger_reason or "none",
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"ifrs9_stage_classifier failed: {e}")
        _log_lesson(f"ifrs9_stage_classifier: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a", encoding="utf-8") as handle:
            handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
