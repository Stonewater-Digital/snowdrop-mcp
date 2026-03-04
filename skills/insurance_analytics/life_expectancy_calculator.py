"""Life expectancy calculator from annual qx rates.

Computes curtate, complete, and temporary life expectancies from a supplied
sequence of annual probabilities of death (qx), following standard
actuarial notation (Bowers et al., "Actuarial Mathematics").
"""
from __future__ import annotations

from typing import Any

from skills.utils import get_iso_timestamp, log_lesson

TOOL_META: dict[str, Any] = {
    "name": "life_expectancy_calculator",
    "description": (
        "Calculates curtate life expectancy (e_x), complete life expectancy (ê_x), "
        "and median future lifetime from a list of annual qx mortality rates. "
        "Uses exact actuarial recursion: t_px = product of (1 - q_{x+k}) for k=0..t-1."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "qx_rates": {
                "type": "array",
                "description": (
                    "Ordered list of annual probabilities of death q_{x}, q_{x+1}, …, q_{x+n-1}. "
                    "Each value must be in [0, 1]. The list represents successive ages from start_age."
                ),
                "items": {"type": "number", "minimum": 0.0, "maximum": 1.0},
                "minItems": 1,
            },
            "start_age": {
                "type": "integer",
                "description": "Attained age corresponding to the first element of qx_rates.",
                "minimum": 0,
                "maximum": 119,
            },
        },
        "required": ["qx_rates", "start_age"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["success", "error"]},
            "curtate_life_expectancy": {
                "type": "number",
                "description": "e_x = sum_{t=1}^{n} t_p_x (expected whole years of future life).",
            },
            "complete_life_expectancy": {
                "type": "number",
                "description": "ê_x ≈ e_x + 0.5 (trapezoidal UDD approximation of complete expectation).",
            },
            "median_future_lifetime": {
                "type": "number",
                "description": "Smallest t such that t_p_x <= 0.5 (median years of future life).",
            },
            "survival_probabilities": {
                "type": "array",
                "description": "t_p_x for t = 0, 1, 2, … from start_age; t_p_x[0] = 1.0.",
                "items": {"type": "number"},
            },
            "terminal_age": {
                "type": "integer",
                "description": "start_age + number of qx periods provided.",
            },
            "timestamp": {"type": "string", "format": "date-time"},
        },
        "required": ["status", "timestamp"],
    },
}


def life_expectancy_calculator(
    qx_rates: list[float],
    start_age: int,
    **_: Any,
) -> dict[str, Any]:
    """Compute life expectancy measures from a sequence of annual qx rates.

    Actuarial definitions used:
      t_p_x = product_{k=0}^{t-1} (1 - q_{x+k})  (probability of surviving t more years)
      e_x   = sum_{t=1}^{omega-x} t_p_x            (curtate life expectancy)
      ê_x   ≈ e_x + 0.5                             (complete LE under UDD assumption)

    The trapezoidal (UDD) approximation of complete life expectancy is:
      ê_x = sum_{t=0}^{n-1} (t_p_x + t+1_p_x) / 2

    Args:
        qx_rates: Annual qx values for ages start_age, start_age+1, …. Each in [0, 1].
        start_age: Attained age at the start of the projection.

    Returns:
        dict with status "success" and life expectancy metrics, or status "error".
    """
    try:
        if not qx_rates:
            raise ValueError("qx_rates must not be empty")
        if start_age < 0 or start_age > 119:
            raise ValueError(f"start_age must be 0–119, got {start_age}")
        for i, q in enumerate(qx_rates):
            if not (0.0 <= q <= 1.0):
                raise ValueError(f"qx_rates[{i}]={q} is outside [0, 1]")

        # Build survival probability sequence: t_p_x for t = 0, 1, …, n
        n = len(qx_rates)
        survival_probs: list[float] = [1.0]
        for qx in qx_rates:
            survival_probs.append(survival_probs[-1] * (1.0 - qx))

        # Curtate life expectancy: e_x = sum of t_p_x for t = 1 to n
        curtate = sum(survival_probs[1:])

        # Complete life expectancy (UDD trapezoidal): ê_x = sum of midpoints
        complete = sum(
            (survival_probs[t] + survival_probs[t + 1]) / 2.0
            for t in range(n)
        )

        # Median future lifetime: smallest t where t_p_x <= 0.5
        median_year = float(n)  # Default: beyond the table
        for idx in range(1, len(survival_probs)):
            if survival_probs[idx] <= 0.5:
                prev_p = survival_probs[idx - 1]
                curr_p = survival_probs[idx]
                # Linear interpolation within the year
                frac = (prev_p - 0.5) / (prev_p - curr_p) if (prev_p - curr_p) > 0 else 0.0
                median_year = (idx - 1) + frac
                break

        return {
            "status": "success",
            "curtate_life_expectancy": round(curtate, 2),
            "complete_life_expectancy": round(complete, 2),
            "median_future_lifetime": round(median_year, 2),
            "survival_probabilities": [round(p, 6) for p in survival_probs],
            "terminal_age": start_age + n,
            "timestamp": get_iso_timestamp(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as exc:
        log_lesson(f"life_expectancy_calculator: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": get_iso_timestamp()}
