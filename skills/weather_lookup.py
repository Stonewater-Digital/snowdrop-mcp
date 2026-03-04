"""
Executive Summary:
    Fetches current weather, multi-day forecasts, and historical weather data via the
    Google Weather API. Resolves human-readable locations (city names, addresses) to
    lat/lng coordinates using the Google Geocoding API before querying weather endpoints.
    Includes a commodity_signal field that flags weather-driven agricultural market
    implications for Thunder's fund accounting and trading workflows.

Inputs:
    action       (str, required)  — "current" | "forecast" | "history"
    location     (str, required)  — city name, address, or "lat,lng"
    days         (int, default 3) — forecast horizon in days (forecast action)
    hours        (int, default 24)— lookback window in hours (history action)
    units        (str, default "metric") — "metric" | "imperial"

Outputs:
    status       (str)  — "ok" | "error"
    data         (dict) — temperature, humidity, wind_speed, conditions,
                          precipitation_probability, uv_index, commodity_signal
    timestamp    (str)  — ISO 8601 UTC

MCP Tool Name: weather_lookup

Agent Notes:
    - Requires GOOGLE_MAPS_API_KEY environment variable (Maps Platform key with
      Weather API and Geocoding API enabled).
    - No GCP service account needed for this skill.
    - commodity_signal is heuristic — agents should treat it as a watch flag,
      not a confirmed trade signal.
    - Rate limits: Google Weather API — 1,000 QPD free tier.
"""

import os
import datetime
import requests

TOOL_META = {
    "name": "weather_lookup",
    "description": (
        "Fetch current weather, multi-day forecasts, or historical weather data "
        "for any location using the Google Weather API. Returns structured weather "
        "metrics plus a commodity_signal field flagging weather-driven market "
        "implications for agricultural futures and supply chain analysis."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": ["current", "forecast", "history"],
                "description": "Weather operation to perform.",
            },
            "location": {
                "type": "string",
                "description": "City name, full address, or 'lat,lng' string.",
            },
            "days": {
                "type": "integer",
                "default": 3,
                "description": "Number of forecast days (forecast action only).",
            },
            "hours": {
                "type": "integer",
                "default": 24,
                "description": "Hours of historical data to retrieve (history action only).",
            },
            "units": {
                "type": "string",
                "enum": ["metric", "imperial"],
                "default": "metric",
                "description": "Unit system for temperature and wind speed.",
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


def _commodity_signal(conditions: str, temp_c: float, precip_pct: float, lat: float) -> str:
    """Heuristic commodity market watch signal derived from weather data."""
    cond = (conditions or "").lower()
    signal_parts = []

    if temp_c < -2 and 25 <= lat <= 50:
        signal_parts.append("Frost risk in mid-latitude grain belt — corn/wheat futures watch")
    if precip_pct > 70 and lat < 35:
        signal_parts.append("Heavy rainfall in lower latitudes — soy/sugarcane disruption possible")
    if "drought" in cond or (precip_pct < 10 and temp_c > 35):
        signal_parts.append("Drought conditions — cattle and feed grain markets may tighten")
    if "storm" in cond or "hurricane" in cond or "typhoon" in cond:
        signal_parts.append("Severe storm system — energy and soft commodity supply disruption risk")
    if "flood" in cond or precip_pct > 85:
        signal_parts.append("Flooding risk — logistics and crop yield pressure likely")

    return "; ".join(signal_parts) if signal_parts else "No significant commodity weather signal detected"


def _parse_forecast_period(period: dict, units: str) -> dict:
    temp_key = "temperature" if units == "metric" else "temperatureF"
    temp = period.get(temp_key, period.get("temperature", {}))
    return {
        "datetime": period.get("displayDateTime", period.get("interval", "")),
        "temperature": temp.get("degrees") if isinstance(temp, dict) else temp,
        "temperature_unit": "C" if units == "metric" else "F",
        "humidity_percent": period.get("relativeHumidity"),
        "wind_speed": period.get("windSpeed", {}).get("value") if isinstance(period.get("windSpeed"), dict) else period.get("windSpeed"),
        "wind_speed_unit": "km/h" if units == "metric" else "mph",
        "conditions": period.get("weatherCondition", period.get("iconCode", "unknown")),
        "precipitation_probability": period.get("precipitationProbability"),
        "uv_index": period.get("uvIndex"),
    }


def weather_lookup(action: str, location: str, days: int = 3, hours: int = 24, units: str = "metric") -> dict:
    api_key = os.environ.get("GOOGLE_MAPS_API_KEY")
    if not api_key:
        return _error("GOOGLE_MAPS_API_KEY environment variable is not set.")

    try:
        coords = _resolve_location(location, api_key)
    except Exception as exc:
        return _error(f"Location resolution failed: {exc}")

    base_url = "https://weather.googleapis.com/v1/forecast:lookup"
    unit_system = "METRIC" if units == "metric" else "IMPERIAL"

    try:
        if action == "current":
            resp = requests.post(
                base_url,
                params={"key": api_key},
                json={"location": coords, "days": 1, "unitsSystem": unit_system},
                timeout=15,
            )
            resp.raise_for_status()
            payload = resp.json()
            current = payload.get("forecastDays", [{}])[0].get("daytimeForecast", {})
            temp = current.get("temperature", {})
            temp_val = temp.get("degrees") if isinstance(temp, dict) else None
            precip = current.get("precipitationProbability", 0) or 0
            conditions_raw = current.get("weatherCondition", "unknown")

            data = {
                "temperature": temp_val,
                "temperature_unit": "C" if units == "metric" else "F",
                "humidity_percent": current.get("relativeHumidity"),
                "wind_speed": current.get("windSpeed", {}).get("value") if isinstance(current.get("windSpeed"), dict) else current.get("windSpeed"),
                "wind_speed_unit": "km/h" if units == "metric" else "mph",
                "conditions": conditions_raw,
                "precipitation_probability": precip,
                "uv_index": current.get("uvIndex"),
                "resolved_location": coords,
                "commodity_signal": _commodity_signal(conditions_raw, temp_val or 20, precip, coords["latitude"]),
            }

        elif action == "forecast":
            resp = requests.post(
                base_url,
                params={"key": api_key},
                json={"location": coords, "days": min(days, 10), "unitsSystem": unit_system},
                timeout=15,
            )
            resp.raise_for_status()
            payload = resp.json()
            forecast_days = payload.get("forecastDays", [])
            periods = []
            for day in forecast_days:
                for period_key in ("daytimeForecast", "overnightForecast"):
                    period = day.get(period_key)
                    if period:
                        parsed = _parse_forecast_period(period, units)
                        parsed["date"] = day.get("displayDate", {})
                        periods.append(parsed)

            first_cond = periods[0].get("conditions", "") if periods else ""
            first_temp = periods[0].get("temperature") or 20 if periods else 20
            first_precip = periods[0].get("precipitation_probability") or 0 if periods else 0

            data = {
                "days_requested": days,
                "periods": periods,
                "resolved_location": coords,
                "commodity_signal": _commodity_signal(first_cond, first_temp, first_precip, coords["latitude"]),
            }

        elif action == "history":
            hist_url = "https://weather.googleapis.com/v1/history:lookup"
            end_time = datetime.datetime.utcnow()
            start_time = end_time - datetime.timedelta(hours=hours)
            resp = requests.post(
                hist_url,
                params={"key": api_key},
                json={
                    "location": coords,
                    "startTime": start_time.isoformat() + "Z",
                    "endTime": end_time.isoformat() + "Z",
                    "unitsSystem": unit_system,
                },
                timeout=15,
            )
            resp.raise_for_status()
            payload = resp.json()
            hourly = payload.get("hours", [])
            parsed_hours = [_parse_forecast_period(h, units) for h in hourly]

            data = {
                "hours_requested": hours,
                "start_time": start_time.isoformat() + "Z",
                "end_time": end_time.isoformat() + "Z",
                "hourly_data": parsed_hours,
                "resolved_location": coords,
                "commodity_signal": "Historical data — no forward-looking commodity signal applicable",
            }

        else:
            return _error(f"Unknown action '{action}'. Must be 'current', 'forecast', or 'history'.")

        return {"status": "ok", "data": data, "timestamp": _now_iso()}

    except requests.HTTPError as exc:
        return _error(f"Google Weather API HTTP error: {exc.response.status_code} — {exc.response.text[:300]}")
    except requests.RequestException as exc:
        return _error(f"Network error contacting Google Weather API: {exc}")
    except Exception as exc:
        return _error(f"Unexpected error in weather_lookup: {exc}")
