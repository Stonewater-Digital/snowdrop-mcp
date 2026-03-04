"""
Executive Summary: Calculates bilateral CVA/DVA for CDS portfolios using marginal default probabilities and exposure profiles.
Inputs: time_points_years (list[float]), positive_exposures (list[float]), negative_exposures (list[float]), discount_factors (list[float]), counterparty_default_probabilities (list[float]), firm_default_probabilities (list[float]), recovery_counterparty (float), recovery_firm (float)
Outputs: status (str), timestamp (str), data (dict)
MCP Tool Name: counterparty_credit_charge
"""
import logging
from datetime import datetime, timezone
from typing import Any, Sequence

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "counterparty_credit_charge",
    "description": (
        "Computes bilateral credit adjustments (CVA/DVA) by integrating discounted exposures with marginal default "
        "probabilities per Basel CVA methodology."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "time_points_years": {
                "type": "array",
                "items": {"type": "number"},
                "description": "Future time buckets in years."
            },
            "positive_exposures": {
                "type": "array",
                "items": {"type": "number"},
                "description": "Expected positive exposure (counterparty owes us) per bucket."
            },
            "negative_exposures": {
                "type": "array",
                "items": {"type": "number"},
                "description": "Expected negative exposure (we owe counterparty) per bucket."
            },
            "discount_factors": {
                "type": "array",
                "items": {"type": "number"},
                "description": "Risk-free discount factors per bucket."
            },
            "counterparty_default_probabilities": {
                "type": "array",
                "items": {"type": "number"},
                "description": "Marginal default probabilities for the counterparty per bucket."
            },
            "firm_default_probabilities": {
                "type": "array",
                "items": {"type": "number"},
                "description": "Marginal default probabilities for our firm per bucket (for DVA)."
            },
            "recovery_counterparty": {
                "type": "number",
                "description": "Counterparty recovery rate."}
            ,
            "recovery_firm": {
                "type": "number",
                "description": "Our own recovery rate."}
        },
        "required": [
            "time_points_years",
            "positive_exposures",
            "negative_exposures",
            "discount_factors",
            "counterparty_default_probabilities",
            "firm_default_probabilities",
            "recovery_counterparty",
            "recovery_firm"
        ]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
            "data": {"type": "object"}
        },
        "required": ["status", "timestamp"]
    }
}


def counterparty_credit_charge(**kwargs: Any) -> dict[str, Any]:
    try:
        times = _clean_vector(kwargs["time_points_years"])
        positive = _clean_vector(kwargs["positive_exposures"])
        negative = _clean_vector(kwargs["negative_exposures"])
        dfs = _clean_vector(kwargs["discount_factors"])
        c_dp = _clean_vector(kwargs["counterparty_default_probabilities"])
        f_dp = _clean_vector(kwargs["firm_default_probabilities"])
        rec_c = float(kwargs["recovery_counterparty"])
        rec_f = float(kwargs["recovery_firm"])
        if not 0 <= rec_c < 1 or not 0 <= rec_f < 1:
            raise ValueError("Recovery rates must lie in [0,1)")
        if not (len(times) == len(positive) == len(negative) == len(dfs) == len(c_dp) == len(f_dp)):
            raise ValueError("All vectors must share the same length")

        cva = 0.0
        dva = 0.0
        expected_positive = 0.0
        expected_negative = 0.0
        for e_pos, e_neg, df, p_c, p_f in zip(positive, negative, dfs, c_dp, f_dp):
            cva += max(e_pos, 0.0) * df * p_c * (1 - rec_c)
            dva += max(-e_neg, 0.0) * df * p_f * (1 - rec_f)
            expected_positive += max(e_pos, 0.0)
            expected_negative += max(-e_neg, 0.0)

        net_charge = cva - dva
        data = {
            "cva": cva,
            "dva": dva,
            "net_credit_charge": net_charge,
            "expected_positive_exposure": expected_positive,
            "expected_negative_exposure": expected_negative
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError, KeyError) as e:
        logger.error("counterparty_credit_charge failed: %s", e)
        _log_lesson(f"counterparty_credit_charge: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


def _clean_vector(values: Sequence[Any]) -> list[float]:
    if not values:
        raise ValueError("Input vectors must be non-empty")
    return [float(v) for v in values]


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a", encoding="utf-8") as file:
            file.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
