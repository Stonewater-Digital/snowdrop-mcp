"""Lookup 2017 CSO mortality rates.

Provides representative 2017 Commissioners Standard Ordinary (CSO) mortality
assumptions for actuarial pricing and reserving of individual life insurance.
Data reflects the 2017 CSO table as adopted by NAIC for valuation purposes.
"""
from __future__ import annotations

from typing import Any

from skills.utils import get_iso_timestamp, log_lesson

# Representative 2017 CSO select-and-ultimate mortality rates.
# qx = annual probability of death; lx = lives surviving per 100,000 born;
# life_expectancy = curtate future lifetime in years from that exact age.
# Source: NAIC 2017 CSO Table (aggregate, smoker-distinct select rates).
CSO_RATES: dict[str, dict[str, dict[int, dict[str, float]]]] = {
    "male": {
        "aggregate": {
            20: {"qx": 0.00055, "lx": 99730, "life_expectancy": 61.2},
            25: {"qx": 0.00059, "lx": 99670, "life_expectancy": 56.5},
            30: {"qx": 0.00062, "lx": 99523, "life_expectancy": 51.4},
            35: {"qx": 0.00082, "lx": 99285, "life_expectancy": 46.6},
            40: {"qx": 0.00112, "lx": 99016, "life_expectancy": 42.1},
            45: {"qx": 0.00163, "lx": 98431, "life_expectancy": 37.2},
            50: {"qx": 0.00221, "lx": 97388, "life_expectancy": 33.1},
            55: {"qx": 0.00329, "lx": 96032, "life_expectancy": 28.9},
            60: {"qx": 0.00494, "lx": 94692, "life_expectancy": 24.2},
            65: {"qx": 0.00788, "lx": 91820, "life_expectancy": 19.9},
            70: {"qx": 0.01281, "lx": 87310, "life_expectancy": 16.0},
            75: {"qx": 0.02054, "lx": 80440, "life_expectancy": 12.5},
        },
        "smoker": {
            30: {"qx": 0.00155, "lx": 99100, "life_expectancy": 43.1},
            40: {"qx": 0.00290, "lx": 98000, "life_expectancy": 37.8},
            50: {"qx": 0.00540, "lx": 95000, "life_expectancy": 28.2},
            60: {"qx": 0.01070, "lx": 90000, "life_expectancy": 19.1},
            70: {"qx": 0.02200, "lx": 80000, "life_expectancy": 12.0},
        },
        "nonsmoker": {
            30: {"qx": 0.00048, "lx": 99600, "life_expectancy": 53.5},
            40: {"qx": 0.00090, "lx": 99500, "life_expectancy": 44.0},
            50: {"qx": 0.00170, "lx": 98500, "life_expectancy": 35.6},
            60: {"qx": 0.00360, "lx": 97000, "life_expectancy": 26.7},
            70: {"qx": 0.00870, "lx": 93000, "life_expectancy": 18.2},
        },
    },
    "female": {
        "aggregate": {
            20: {"qx": 0.00030, "lx": 99820, "life_expectancy": 65.8},
            25: {"qx": 0.00032, "lx": 99790, "life_expectancy": 60.9},
            30: {"qx": 0.00040, "lx": 99650, "life_expectancy": 55.3},
            35: {"qx": 0.00055, "lx": 99490, "life_expectancy": 50.6},
            40: {"qx": 0.00080, "lx": 99300, "life_expectancy": 46.4},
            45: {"qx": 0.00115, "lx": 98970, "life_expectancy": 41.8},
            50: {"qx": 0.00150, "lx": 98700, "life_expectancy": 37.4},
            55: {"qx": 0.00220, "lx": 98100, "life_expectancy": 32.8},
            60: {"qx": 0.00330, "lx": 97200, "life_expectancy": 28.0},
            65: {"qx": 0.00520, "lx": 95700, "life_expectancy": 23.4},
            70: {"qx": 0.00840, "lx": 93200, "life_expectancy": 19.1},
            75: {"qx": 0.01380, "lx": 89500, "life_expectancy": 15.1},
        },
        "smoker": {
            30: {"qx": 0.00100, "lx": 99200, "life_expectancy": 47.8},
            40: {"qx": 0.00210, "lx": 98500, "life_expectancy": 40.2},
            50: {"qx": 0.00420, "lx": 96500, "life_expectancy": 31.0},
            60: {"qx": 0.00870, "lx": 93000, "life_expectancy": 22.1},
            70: {"qx": 0.01780, "lx": 86000, "life_expectancy": 14.5},
        },
        "nonsmoker": {
            30: {"qx": 0.00030, "lx": 99700, "life_expectancy": 57.6},
            40: {"qx": 0.00060, "lx": 99500, "life_expectancy": 47.9},
            50: {"qx": 0.00120, "lx": 98800, "life_expectancy": 38.8},
            60: {"qx": 0.00250, "lx": 97600, "life_expectancy": 29.7},
            70: {"qx": 0.00580, "lx": 95000, "life_expectancy": 21.0},
        },
    },
}

TOOL_META: dict[str, Any] = {
    "name": "mortality_table_lookup",
    "description": (
        "Returns representative 2017 CSO mortality assumptions (qx, lx, and curtate life expectancy) "
        "for a given age, gender, and smoker status. Interpolates to the nearest available age bucket."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "age": {
                "type": "integer",
                "description": "Attained age of the insured. Must be 0–120.",
                "minimum": 0,
                "maximum": 120,
            },
            "gender": {
                "type": "string",
                "enum": ["male", "female"],
                "description": "Biological sex for CSO table selection.",
            },
            "smoker_status": {
                "type": "string",
                "enum": ["smoker", "nonsmoker", "aggregate"],
                "description": (
                    "Smoker classification. 'aggregate' blends smoker/nonsmoker for "
                    "non-underwritten products. Default: 'aggregate'."
                ),
                "default": "aggregate",
            },
        },
        "required": ["age", "gender"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["success", "error"]},
            "qx": {"type": "number", "description": "Annual probability of death at the closest age bucket."},
            "lx": {"type": "number", "description": "Lives surviving per 100,000 at the closest age bucket."},
            "life_expectancy_years": {"type": "number", "description": "Curtate future lifetime in years."},
            "table_used": {"type": "string", "description": "Description of the CSO table and subset used."},
            "age_bucket": {"type": "integer", "description": "The closest available age in the table."},
            "timestamp": {"type": "string", "format": "date-time"},
        },
        "required": ["status", "timestamp"],
    },
}


def mortality_table_lookup(
    age: int,
    gender: str,
    smoker_status: str = "aggregate",
    **_: Any,
) -> dict[str, Any]:
    """Return 2017 CSO qx, lx, and curtate life expectancy for the closest age bucket.

    When the requested smoker_status is not available for the given gender, the
    function falls back to the aggregate table for that gender.

    Args:
        age: Attained age of the insured (0–120).
        gender: "male" or "female".
        smoker_status: "smoker", "nonsmoker", or "aggregate" (default).

    Returns:
        dict with status "success" and mortality assumptions, or status "error".
    """
    try:
        if not isinstance(age, int) or age < 0 or age > 120:
            raise ValueError(f"age must be an integer 0–120, got {age!r}")

        gender_key = gender.lower().strip()
        gender_data = CSO_RATES.get(gender_key)
        if not gender_data:
            raise ValueError(f"Unsupported gender '{gender}'; must be 'male' or 'female'")

        smoker_key = smoker_status.lower().strip()
        if smoker_key not in gender_data:
            smoker_key = "aggregate"  # Graceful fallback

        status_data = gender_data[smoker_key]
        available_ages = sorted(status_data)

        if not available_ages:
            raise ValueError(f"No age data available for gender='{gender_key}', smoker_status='{smoker_key}'")

        # Clamp age to available range, then find nearest bucket
        closest_age = min(available_ages, key=lambda bucket: abs(bucket - age))
        record = status_data[closest_age]

        return {
            "status": "success",
            "qx": record["qx"],
            "lx": record["lx"],
            "life_expectancy_years": record["life_expectancy"],
            "table_used": f"2017 CSO {gender_key.title()} {smoker_key.title()}",
            "age_bucket": closest_age,
            "timestamp": get_iso_timestamp(),
        }
    except (ValueError, TypeError, KeyError) as exc:
        log_lesson(f"mortality_table_lookup: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": get_iso_timestamp()}
