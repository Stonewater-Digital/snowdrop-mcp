"""
Execuve Summary: Evaluates distribution shape via skewness, kurtosis, and Jarque-Bera statistic.
Inputs: returns (list[float])
Outputs: skewness (float), kurtosis (float), excess_kurtosis (float), jarque_bera_stat (float), is_normal (bool), distribution_description (str)
MCP Tool Name: skewness_kurtosis_analyzer
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "skewness_kurtosis_analyzer",
    "description": "Computes skewness, kurtosis, and Jarque-Bera statistic for return distributions.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "returns": {"type": "array", "description": "Return series."}
        },
        "required": ["returns"]
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "timestamp": {"type": "string"}, "data": {"type": "object"}}, "required": ["status", "timestamp"]
    }
}


def skewness_kurtosis_analyzer(**kwargs: Any) -> dict:
    """Measures higher moments and Jarque-Bera normality test."""
    try:
        returns = kwargs.get("returns")
        if not isinstance(returns, list) or len(returns) < 5:
            raise ValueError("returns must contain at least five observations")
        values = [float(r) for r in returns]
        n = len(values)
        mean_val = sum(values) / n
        variance = sum((x - mean_val) ** 2 for x in values) / n
        std_dev = math.sqrt(variance)
        skewness = (sum((x - mean_val) ** 3 for x in values) / n) / (std_dev ** 3 if std_dev else 1)
        kurtosis = (sum((x - mean_val) ** 4 for x in values) / n) / (std_dev ** 4 if std_dev else 1)
        excess_kurtosis = kurtosis - 3
        jarque_bera = (n / 6) * (skewness ** 2 + (excess_kurtosis ** 2) / 4)
        is_normal = jarque_bera < 5.99  # chi-square with 2 dof at 95%
        if skewness > 0.5:
            description = "right_skewed"
        elif skewness < -0.5:
            description = "left_skewed"
        else:
            description = "approximately_symmetrical"
        if not is_normal:
            description += "_non_normal"

        return {
            "status": "success",
            "data": {
                "skewness": skewness,
                "kurtosis": kurtosis,
                "excess_kurtosis": excess_kurtosis,
                "jarque_bera_stat": jarque_bera,
                "is_normal": is_normal,
                "distribution_description": description
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"skewness_kurtosis_analyzer failed: {e}")
        _log_lesson(f"skewness_kurtosis_analyzer: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
