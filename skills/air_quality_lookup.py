"""
Executive Summary:
    Fetches real-time and historical air quality data via the Google Air Quality API
    for use in ESG scoring, real estate valuation, and health-risk analysis. Returns
    structured AQI metrics, dominant pollutant data, and health recommendations. Derives
    a 0–100 esg_score (100 = pristine air, 0 = hazardous) and a real_estate_impact
    string for integration into Thunder's fund accounting and property investment
    workflows.

Inputs:
    action         (str, required)  — "current" | "history" | "heatmap_tile"
    location       (str, required)  — "lat,lng" or human-readable address
    hours          (int, default 24)— lookback window in hours (history action)
    language_code  (str, default "en") — BCP-47 language for health recommendations

Outputs:
    status              (str)  — "ok" | "error"
    data                (dict) — aqi, dominant_pollutant, health_category,
                                 health_recommendations, pollutants,
                                 esg_score, real_estate_impact
    timestamp           (str)  — ISO 8601 UTC

MCP Tool Name: air_quality_lookup

Agent Notes:
    - Requires GOOGLE_MAPS_API_KEY with Air Quality API enabled.
    - GCP service account is NOT required; API key auth is sufficient.
    - esg_score derivation: score = max(0, 100 - aqi) capped to [0, 100].
      Universal AQI (UAQI) scale used by Google (0=hazardous, 100=excellent).
      For UAQI the raw value IS the score; for US AQI we invert.
    - heatmap_tile action returns the tile URL template only — the actual
      PNG tile must be fetched client-side for rendering.
    - history action calls the hourlyHistory endpoint and returns per-hour
      AQI snapshots; large hour counts may be slow.
    - Rate limits: Air Quality API — see GCP project quota dashboard.
"""

import os
import datetime
import requests

TOOL_META = {
    "name": "air_quality_lookup",
    "description": (
        "Retrieve current air quality conditions, historical hourly AQI data, or "
        "heatmap tile configuration for any location using the Google Air Quality API. "
        "Returns AQI score, dominant pollutant, individual pollutant concentrations, "
        "health recommendations, plus an esg_score (0–100) and real_estate_impact "
        "assessment for ESG reporting and property valuation workflows."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": ["current", "history", "heatmap_tile"],
                "description": "Air quality operation to perform.",
            },
            "location": {
                "type": "string",
                "description": "'lat,lng' string or human-readable address.",
            },
            "hours": {
                "type": "integer",
                "default": 24,
                "description": "Hours of historical AQI data to retrieve (history action).",
            },
            "language_code": {
                "type": "string",
                "default": "en",
                "description": "BCP-47 language code for health recommendations text.",
            },
        },
        "required": ["action", "location"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {"type": "object"},
            "timestamp": {"type": "string"},
        },
    },
}

_EXTRA_COMPUTATIONS = [
    "HEALTH_RECOMMENDATIONS",
    "DOMINANT_POLLUTANT_CONCENTRATION",
    "POLLUTANT_ADDITIONAL_INFO",
]


def _now_iso() -> str:
    return datetime.datetime.utcnow().isoformat() + "Z"


def _error(msg: str) -> dict:
    return {"status": "error", "data": {"message": msg}, "timestamp": _now_iso()}


def _resolve_location(location: str, api_key: str) -> dict:
    """Return {"latitude": float, "longitude": float} from a location string."""
    parts = [p.strip() for p in location.split(",")]
    if len(parts) == 2:
        try:
            return {"latitude": float(parts[0]), "longitude": float(parts[1])}
        except ValueError:
            pass

    geo_url = "https://maps.googleapis.com/maps/api/geocode/json"
    resp = requests.get(geo_url, params={"address": location, "key": api_key}, timeout=10)
    resp.raise_for_status()
    results = resp.json().get("results", [])
    if not results:
        raise ValueError(f"Geocoding returned no results for: {location}")
    loc = results[0]["geometry"]["location"]
    return {"latitude": loc["lat"], "longitude": loc["lng"]}


def _derive_esg_score(indexes: list) -> int:
    """
    Derive ESG air quality score 0–100 from Google AQI index list.
    Google's Universal AQI (UAQI) is already 0–100 where 100 = excellent.
    US AQI is 0–500 where 0 = good, 500 = hazardous (inverted).
    Prefer UAQI when available; fall back to inverting US AQI.
    """
    if not indexes:
        return 50  # neutral default when no data

    uaqi = next((ix for ix in indexes if ix.get("code") == "uaqi"), None)
    if uaqi and uaqi.get("aqi") is not None:
        return max(0, min(100, int(uaqi["aqi"])))

    us_aqi = next((ix for ix in indexes if ix.get("code") == "usa_epa"), None)
    if us_aqi and us_aqi.get("aqi") is not None:
        raw = int(us_aqi["aqi"])
        return max(0, min(100, 100 - int(raw / 5)))

    # Generic fallback: use first available index
    first = indexes[0]
    raw = first.get("aqi", 50)
    if raw <= 100:
        return max(0, min(100, 100 - raw))
    return max(0, min(100, 100 - int(raw / 5)))


def _real_estate_impact(esg_score: int, health_category: str) -> str:
    """Heuristic real estate impact statement based on air quality ESG score."""
    if esg_score >= 85:
        return (
            f"Excellent air quality (ESG score {esg_score}/100) — positive premium driver "
            "for residential and mixed-use properties; supports higher asking rents and "
            "lower vacancy in health-conscious submarkets."
        )
    elif esg_score >= 65:
        return (
            f"Good air quality (ESG score {esg_score}/100) — neutral to slightly positive "
            "effect on property values; no material discount expected from air quality alone."
        )
    elif esg_score >= 40:
        return (
            f"Moderate air quality (ESG score {esg_score}/100) — may apply a 2–5% discount "
            "to residential cap rates vs. comparable clean-air submarkets; monitor trends."
        )
    elif esg_score >= 20:
        return (
            f"Poor air quality (ESG score {esg_score}/100) — likely 5–15% discount on "
            "residential values; institutional ESG mandates may restrict investment; "
            "industrial/logistics use cases less affected."
        )
    else:
        return (
            f"Hazardous air quality (ESG score {esg_score}/100) — significant headwind "
            "for any residential or mixed-use investment; regulatory and liability risk "
            "elevated; due diligence must include environmental remediation assessment."
        )


def _parse_indexes(indexes: list) -> dict:
    """Extract a clean summary from the AQI indexes list."""
    result = {}
    for ix in indexes:
        code = ix.get("code", "unknown")
        result[code] = {
            "aqi": ix.get("aqi"),
            "category": ix.get("category"),
            "dominant_pollutant": ix.get("dominantPollutant"),
            "display_name": ix.get("displayName", code),
        }
    return result


def _parse_pollutants(pollutants: list) -> list:
    """Normalize pollutant list to clean dicts."""
    cleaned = []
    for p in pollutants:
        conc = p.get("concentration", {})
        cleaned.append({
            "code": p.get("code", ""),
            "display_name": p.get("displayName", ""),
            "concentration_value": conc.get("value") if isinstance(conc, dict) else None,
            "concentration_units": conc.get("units", "") if isinstance(conc, dict) else "",
            "full_name": p.get("fullName", ""),
        })
    return cleaned


def _parse_current_payload(payload: dict, esg_score: int, health_category: str) -> dict:
    indexes = payload.get("indexes", [])
    pollutants = payload.get("pollutants", [])
    recs = payload.get("healthRecommendations", {})

    primary_index = next(
        (ix for ix in indexes if ix.get("code") == "uaqi"),
        indexes[0] if indexes else {},
    )

    return {
        "aqi": primary_index.get("aqi"),
        "aqi_index": primary_index.get("code", "uaqi"),
        "health_category": primary_index.get("category", health_category),
        "dominant_pollutant": primary_index.get("dominantPollutant"),
        "all_indexes": _parse_indexes(indexes),
        "pollutants": _parse_pollutants(pollutants),
        "health_recommendations": recs,
        "esg_score": esg_score,
    }


def air_quality_lookup(
    action: str,
    location: str,
    hours: int = 24,
    language_code: str = "en",
) -> dict:
    api_key = os.environ.get("GOOGLE_MAPS_API_KEY")
    if not api_key:
        return _error("GOOGLE_MAPS_API_KEY environment variable is not set.")

    try:
        coords = _resolve_location(location, api_key)
    except Exception as exc:
        return _error(f"Location resolution failed: {exc}")

    try:
        if action == "current":
            resp = requests.post(
                "https://airquality.googleapis.com/v1/currentConditions:lookup",
                params={"key": api_key},
                json={
                    "location": coords,
                    "extraComputations": _EXTRA_COMPUTATIONS,
                    "languageCode": language_code,
                },
                timeout=15,
            )
            resp.raise_for_status()
            payload = resp.json()

            indexes = payload.get("indexes", [])
            esg_score = _derive_esg_score(indexes)
            primary = next((ix for ix in indexes if ix.get("code") == "uaqi"), indexes[0] if indexes else {})
            health_category = primary.get("category", "Unknown")

            data = _parse_current_payload(payload, esg_score, health_category)
            data["resolved_location"] = coords
            data["real_estate_impact"] = _real_estate_impact(esg_score, health_category)

            return {"status": "ok", "data": data, "timestamp": _now_iso()}

        elif action == "history":
            hours = max(1, min(hours, 720))  # API supports up to 720 hours
            end_time = datetime.datetime.utcnow()
            start_time = end_time - datetime.timedelta(hours=hours)

            # hourlyHistory uses pagination; collect all pages
            all_hours = []
            page_token = None
            page_count = 0

            while True:
                body = {
                    "location": coords,
                    "period": {
                        "startTime": start_time.isoformat() + "Z",
                        "endTime": end_time.isoformat() + "Z",
                    },
                    "extraComputations": _EXTRA_COMPUTATIONS,
                    "languageCode": language_code,
                    "pageSize": 24,
                }
                if page_token:
                    body["pageToken"] = page_token

                resp = requests.post(
                    "https://airquality.googleapis.com/v1/history:lookup",
                    params={"key": api_key},
                    json=body,
                    timeout=20,
                )
                resp.raise_for_status()
                page_data = resp.json()
                all_hours.extend(page_data.get("hoursInfo", []))
                page_token = page_data.get("nextPageToken")
                page_count += 1
                if not page_token or page_count > 30:
                    break

            parsed_hours = []
            for hour_entry in all_hours:
                indexes = hour_entry.get("indexes", [])
                esg_score = _derive_esg_score(indexes)
                primary = next((ix for ix in indexes if ix.get("code") == "uaqi"), indexes[0] if indexes else {})
                parsed_hours.append({
                    "date_time": hour_entry.get("dateTime", ""),
                    "aqi": primary.get("aqi"),
                    "health_category": primary.get("category", "Unknown"),
                    "dominant_pollutant": primary.get("dominantPollutant"),
                    "esg_score": esg_score,
                    "pollutants": _parse_pollutants(hour_entry.get("pollutants", [])),
                })

            aqi_values = [h["aqi"] for h in parsed_hours if h.get("aqi") is not None]
            avg_aqi = round(sum(aqi_values) / len(aqi_values), 1) if aqi_values else None
            avg_esg = round(sum(h["esg_score"] for h in parsed_hours) / len(parsed_hours), 1) if parsed_hours else 50

            return {
                "status": "ok",
                "data": {
                    "action": "history",
                    "resolved_location": coords,
                    "hours_requested": hours,
                    "start_time": start_time.isoformat() + "Z",
                    "end_time": end_time.isoformat() + "Z",
                    "records_returned": len(parsed_hours),
                    "average_aqi": avg_aqi,
                    "average_esg_score": avg_esg,
                    "hourly_data": parsed_hours,
                    "real_estate_impact": _real_estate_impact(int(avg_esg), "Historical Average"),
                },
                "timestamp": _now_iso(),
            }

        elif action == "heatmap_tile":
            # Returns the URL template for Air Quality heatmap tiles (PNG)
            # Tile URL: https://airquality.googleapis.com/v1/mapTypes/{mapType}/heatmapTiles/{zoom}/{x}/{y}
            # Clients use this template to fetch individual tiles for rendering.
            tile_url_template = (
                "https://airquality.googleapis.com/v1/mapTypes/UAQI_INDIGO_PERSIAN"
                "/heatmapTiles/{zoom}/{x}/{y}?key=" + api_key
            )
            available_map_types = [
                "UAQI_INDIGO_PERSIAN",
                "UAQI_RED_GREEN",
                "PM25_INDIGO_PERSIAN",
                "GBR_DEFRA",
                "DEU_UBA",
                "CAN_EC",
                "FRA_ATMO",
                "IND_CPCB",
                "AUS_AQICN",
                "US_AQI",
            ]
            return {
                "status": "ok",
                "data": {
                    "action": "heatmap_tile",
                    "resolved_location": coords,
                    "tile_url_template": tile_url_template,
                    "zoom_range": {"min": 0, "max": 16},
                    "available_map_types": available_map_types,
                    "usage_note": (
                        "Replace {zoom}, {x}, {y} with integer tile coordinates. "
                        "Tiles are PNG images suitable for map overlay rendering. "
                        "API key is embedded in the URL template — treat as sensitive."
                    ),
                    "esg_score": None,
                    "real_estate_impact": (
                        "Heatmap tiles provide visual AQI context for site selection "
                        "and portfolio mapping; fetch current or history for numeric ESG score."
                    ),
                },
                "timestamp": _now_iso(),
            }

        else:
            return _error(f"Unknown action '{action}'. Must be 'current', 'history', or 'heatmap_tile'.")

    except requests.HTTPError as exc:
        return _error(f"Google Air Quality API HTTP error: {exc.response.status_code} — {exc.response.text[:300]}")
    except requests.RequestException as exc:
        return _error(f"Network error contacting Google Air Quality API: {exc}")
    except Exception as exc:
        return _error(f"Unexpected error in air_quality_lookup: {exc}")
