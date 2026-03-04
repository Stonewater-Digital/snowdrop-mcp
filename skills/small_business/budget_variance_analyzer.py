"""
Executive Smary: Calculates budget vs actual variances and highlights overruns/savings.
Inputs: budget_items (list)
Outputs: variance_per_item (list), favorable_unfavorable (dict), total_variance (float), largest_overruns (list), largest_savings (list)
MCP Tool Name: budget_variance_analyzer
"""
import logging
from datetime import datetime, timezone
from typing import Any, List, Dict

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "budget_variance_analyzer",
    "description": (
        "Summarizes budgeted versus actual spend by category with variance breakdowns, "
        "flagging overruns and savings opportunities."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "budget_items": {
                "type": "array",
                "description": "List of items {category, budgeted, actual}.",
                "items": {"type": "object"},
            }
        },
        "required": ["budget_items"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
            "data": {"type": "object"},
        },
        "required": ["status", "timestamp"],
    },
}


def budget_variance_analyzer(**kwargs: Any) -> dict:
    """Analyze budget variance and highlight major variances."""
    try:
        items = kwargs["budget_items"]
        if not isinstance(items, list):
            raise ValueError("budget_items must be a list")

        variances: List[Dict[str, Any]] = []
        overruns: List[Dict[str, Any]] = []
        savings: List[Dict[str, Any]] = []
        total_variance = 0.0

        for entry in items:
            category = str(entry["category"])
            budgeted = float(entry["budgeted"])
            actual = float(entry["actual"])
            variance = actual - budgeted
            pct = variance / budgeted if budgeted else float("inf")
            record = {"category": category, "variance": variance, "variance_pct": pct}
            variances.append(record)
            total_variance += variance
            if variance > 0:
                overruns.append(record)
            else:
                savings.append(record)

        largest_overruns = sorted(overruns, key=lambda x: x["variance"], reverse=True)[:3]
        largest_savings = sorted(savings, key=lambda x: x["variance"])[:3]
        f_u = {"overruns": len(overruns), "savings": len(savings)}

        return {
            "status": "success",
            "data": {
                "variance_per_item": variances,
                "favorable_unfavorable": f_u,
                "total_variance": total_variance,
                "largest_overruns": largest_overruns,
                "largest_savings": largest_savings,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError, KeyError) as e:
        logger.error(f"budget_variance_analyzer failed: {e}")
        _log_lesson(f"budget_variance_analyzer: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
