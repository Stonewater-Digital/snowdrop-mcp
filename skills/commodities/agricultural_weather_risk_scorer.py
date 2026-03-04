"""Score crop weather risk across regions."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Iterable

TOOL_META: dict[str, Any] = {
    "name": "agricultural_weather_risk_scorer",
    "description": (
        "Scores crop yield risk from precipitation and temperature anomalies across agricultural "
        "regions. Returns risk scores (0–10), identifies the highest-risk region, and provides "
        "an aggregate supply disruption probability estimate."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "regions": {
                "type": "array",
                "description": "List of regions with weather anomaly data.",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Region or country name.",
                        },
                        "rainfall_deviation_pct": {
                            "type": "number",
                            "description": (
                                "Rainfall deviation from seasonal normal in %. "
                                "Negative = drought, positive = flood risk."
                            ),
                        },
                        "temperature_deviation_c": {
                            "type": "number",
                            "description": "Temperature deviation from seasonal normal in °C.",
                        },
                        "soil_moisture_pct": {
                            "type": "number",
                            "default": 30,
                            "description": "Current soil moisture as % of field capacity (0–100). Defaults to 30.",
                        },
                        "crop_growth_stage": {
                            "type": "string",
                            "default": "vegetative",
                            "enum": ["germination", "vegetative", "flowering", "grain_fill", "harvest"],
                            "description": "Crop growth stage — sensitive stages amplify risk. Defaults to 'vegetative'.",
                        },
                    },
                    "required": ["name", "rainfall_deviation_pct", "temperature_deviation_c"],
                },
                "minItems": 1,
            }
        },
        "required": ["regions"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["success", "error"]},
            "region_scores": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "risk_score": {"type": "number"},
                        "risk_level": {"type": "string"},
                        "rainfall_contribution": {"type": "number"},
                        "temperature_contribution": {"type": "number"},
                    },
                },
            },
            "highest_risk_region": {"type": "object"},
            "average_score": {"type": "number"},
            "high_risk_region_count": {"type": "integer"},
            "timestamp": {"type": "string"},
        },
    },
}

# Growth stage risk multipliers: sensitive stages amplify weather impacts
_STAGE_MULTIPLIERS = {
    "germination": 1.2,
    "vegetative": 1.0,
    "flowering": 1.5,
    "grain_fill": 1.4,
    "harvest": 0.8,
}


def agricultural_weather_risk_scorer(
    regions: Iterable[dict[str, Any]],
    **_: Any,
) -> dict[str, Any]:
    """Return stress score per region and top risks.

    Args:
        regions: Iterable of region dicts with rainfall_deviation_pct,
            temperature_deviation_c, optional soil_moisture_pct, and crop_growth_stage.

    Returns:
        dict with status, region_scores (0–10 each), highest_risk_region,
        average_score, and high_risk_region_count (score >= 6).

    Scoring formula:
        rainfall_contribution  = |rainfall_deviation_pct| / 10
        temperature_contribution = |temperature_deviation_c| / 2
        soil_bonus = max(0, (soil_moisture_pct - 40) / 20)  # excess moisture reduces risk
        raw_score = (rainfall_contribution + temperature_contribution - soil_bonus)
                    * stage_multiplier
        risk_score = clamp(raw_score, 0, 10)

    Risk levels:
        low:    0–3
        medium: 3–6
        high:   6–10
    """
    try:
        region_list = list(regions)
        if not region_list:
            raise ValueError("regions cannot be empty")

        scores = []
        for region in region_list:
            name = str(region["name"])
            rainfall_dev = float(region["rainfall_deviation_pct"])
            temp_dev = float(region["temperature_deviation_c"])
            soil = float(region.get("soil_moisture_pct", 30))
            stage = str(region.get("crop_growth_stage", "vegetative")).lower()

            if not 0 <= soil <= 100:
                raise ValueError(f"soil_moisture_pct must be 0–100 for region '{name}', got {soil}")

            stage_mult = _STAGE_MULTIPLIERS.get(stage, 1.0)

            rainfall_contribution = abs(rainfall_dev) / 10.0
            temp_contribution = abs(temp_dev) / 2.0
            # Soil bonus: well-watered fields (>40% capacity) reduce risk slightly
            soil_bonus = max(0.0, (soil - 40.0) / 20.0)

            raw_score = (rainfall_contribution + temp_contribution - soil_bonus) * stage_mult
            risk_score = min(10.0, max(0.0, raw_score))

            if risk_score < 3.0:
                risk_level = "low"
            elif risk_score < 6.0:
                risk_level = "medium"
            else:
                risk_level = "high"

            scores.append(
                {
                    "name": name,
                    "risk_score": round(risk_score, 2),
                    "risk_level": risk_level,
                    "rainfall_contribution": round(rainfall_contribution, 3),
                    "temperature_contribution": round(temp_contribution, 3),
                }
            )

        worst = max(scores, key=lambda item: item["risk_score"])
        avg = sum(item["risk_score"] for item in scores) / len(scores)
        high_risk_count = sum(1 for item in scores if item["risk_score"] >= 6.0)

        return {
            "status": "success",
            "region_scores": scores,
            "highest_risk_region": worst,
            "average_score": round(avg, 2),
            "high_risk_region_count": high_risk_count,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("agricultural_weather_risk_scorer", str(exc))
        return {
            "status": "error",
            "error": str(exc),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
