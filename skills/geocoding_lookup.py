"""
Executive Summary:
    Google Geocoding API skill for address normalization, coordinate lookup, address validation,
    and timezone resolution. Critical for real estate workflows, property valuation pipelines,
    and any location-aware financial analysis within Snowdrop Core.

Inputs:
    action    (str, required)   — "geocode" | "reverse_geocode" | "validate" | "timezone"
    address   (str)             — Street address string (geocode / validate actions)
    latitude  (float)           — Decimal latitude (reverse_geocode / timezone actions)
    longitude (float)           — Decimal longitude (reverse_geocode / timezone actions)
    language  (str, default "en") — BCP-47 language tag for response localization
    region    (str, optional)   — CLDR region code to bias results (e.g. "us", "gb")

Outputs:
    {"status": "ok"|"error", "data": {action-specific fields, "geospatial_context": str}, "timestamp": ISO8601}

MCP Tool Name: geocoding_lookup

Agent Notes:
    - API key sourced exclusively from GOOGLE_MAPS_API_KEY environment variable
    - geocode returns: lat, lng, formatted_address, place_id, address_components, location_type
    - reverse_geocode returns: formatted_address, address_components dict (street/city/state/zip/country)
    - validate uses Address Validation API (POST); returns verdict and standardized address
    - timezone uses the Time Zone API with current Unix timestamp as reference
    - geospatial_context is a brief string noting financial/geographic significance of the location
"""

import os
import time

import requests

from skills.utils import get_iso_timestamp, memory_cache

TOOL_META = {
    "name": "geocoding_lookup",
    "description": (
        "Google Geocoding API skill for address normalization, coordinate lookup, "
        "address validation, and timezone resolution. Used in real estate and "
        "location-based financial analysis pipelines."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": ["geocode", "reverse_geocode", "validate", "timezone"],
                "description": "The geocoding operation to perform."
            },
            "address": {
                "type": "string",
                "description": "Street address string (required for geocode and validate)."
            },
            "latitude": {
                "type": "number",
                "description": "Decimal latitude (required for reverse_geocode and timezone)."
            },
            "longitude": {
                "type": "number",
                "description": "Decimal longitude (required for reverse_geocode and timezone)."
            },
            "language": {
                "type": "string", "default": "en",
                "description": "BCP-47 language tag for API response localization."
            },
            "region": {
                "type": "string",
                "description": "CLDR region code to bias geocoding results (e.g. 'us')."
            }
        },
        "required": ["action"]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["ok", "error"]},
            "data": {"type": "object"},
            "timestamp": {"type": "string", "format": "date-time"}
        },
        "required": ["status", "data", "timestamp"]
    }
}


def _ts() -> str:
    return get_iso_timestamp()


def _api_key() -> str:
    key = os.environ.get("GOOGLE_MAPS_API_KEY")
    if not key:
        raise EnvironmentError("GOOGLE_MAPS_API_KEY environment variable is not set.")
    return key


def _extract_component(components: list, ctype: str) -> str:
    for c in components:
        if ctype in c.get("types", []):
            return c.get("long_name", "")
    return ""


def _geospatial_context(formatted: str, components: list) -> str:
    country = _extract_component(components, "country")
    state = _extract_component(components, "administrative_area_level_1")
    locality = _extract_component(components, "locality")
    parts = [p for p in [locality, state, country] if p]
    loc = ", ".join(parts) if parts else formatted
    return f"Location resolved to {loc}. Suitable for regional pricing, tax jurisdiction, and compliance zone determination."


@memory_cache(ttl_seconds=86400)
def geocoding_lookup(
    action: str,
    address: str = None,
    latitude: float = None,
    longitude: float = None,
    language: str = "en",
    region: str = None
) -> dict:
    """Execute a Google Maps geocoding, validation, or timezone operation."""
    try:
        key = _api_key()

        if action == "geocode":
            if not address:
                return {"status": "error", "data": {"error": "address is required for geocode."}, "timestamp": _ts()}
            params = {"address": address, "language": language, "key": key}
            if region:
                params["region"] = region
            resp = requests.get("https://maps.googleapis.com/maps/api/geocode/json", params=params, timeout=10)
            resp.raise_for_status()
            body = resp.json()
            if body.get("status") != "OK" or not body.get("results"):
                return {"status": "error", "data": {"error": body.get("status", "NO_RESULTS"), "raw": body.get("error_message", "")}, "timestamp": _ts()}
            result = body["results"][0]
            loc = result["geometry"]["location"]
            comps = result.get("address_components", [])
            data = {
                "lat": loc["lat"], "lng": loc["lng"],
                "formatted_address": result["formatted_address"],
                "place_id": result.get("place_id"),
                "location_type": result["geometry"].get("location_type"),
                "address_components": {
                    "street_number": _extract_component(comps, "street_number"),
                    "route": _extract_component(comps, "route"),
                    "city": _extract_component(comps, "locality"),
                    "state": _extract_component(comps, "administrative_area_level_1"),
                    "zip": _extract_component(comps, "postal_code"),
                    "country": _extract_component(comps, "country")
                },
                "geospatial_context": _geospatial_context(result["formatted_address"], comps)
            }
            return {"status": "ok", "data": data, "timestamp": _ts()}

        if action == "reverse_geocode":
            if latitude is None or longitude is None:
                return {"status": "error", "data": {"error": "latitude and longitude required for reverse_geocode."}, "timestamp": _ts()}
            params = {"latlng": f"{latitude},{longitude}", "language": language, "key": key}
            resp = requests.get("https://maps.googleapis.com/maps/api/geocode/json", params=params, timeout=10)
            resp.raise_for_status()
            body = resp.json()
            if body.get("status") != "OK" or not body.get("results"):
                return {"status": "error", "data": {"error": body.get("status", "NO_RESULTS")}, "timestamp": _ts()}
            result = body["results"][0]
            comps = result.get("address_components", [])
            data = {
                "formatted_address": result["formatted_address"],
                "place_id": result.get("place_id"),
                "address_components": {
                    "street_number": _extract_component(comps, "street_number"),
                    "route": _extract_component(comps, "route"),
                    "city": _extract_component(comps, "locality"),
                    "state": _extract_component(comps, "administrative_area_level_1"),
                    "zip": _extract_component(comps, "postal_code"),
                    "country": _extract_component(comps, "country")
                },
                "geospatial_context": _geospatial_context(result["formatted_address"], comps)
            }
            return {"status": "ok", "data": data, "timestamp": _ts()}

        if action == "validate":
            if not address:
                return {"status": "error", "data": {"error": "address is required for validate."}, "timestamp": _ts()}
            url = f"https://addressvalidation.googleapis.com/v1:validateAddress?key={key}"
            payload = {"address": {"addressLines": [address]}}
            if region:
                payload["address"]["regionCode"] = region.upper()
            resp = requests.post(url, json=payload, timeout=10)
            resp.raise_for_status()
            body = resp.json()
            result = body.get("result", {})
            verdict = result.get("verdict", {})
            postal = result.get("address", {})
            data = {
                "has_unconfirmed_components": verdict.get("hasUnconfirmedComponents", False),
                "address_complete": verdict.get("addressComplete", False),
                "validation_granularity": verdict.get("validationGranularity"),
                "standardized_address": postal.get("formattedAddress"),
                "missing_component_types": verdict.get("missingComponentTypes", []),
                "geospatial_context": (
                    f"Address validation complete. Granularity: {verdict.get('validationGranularity', 'unknown')}. "
                    "Use standardized_address for downstream record normalization."
                )
            }
            return {"status": "ok", "data": data, "timestamp": _ts()}

        if action == "timezone":
            if latitude is None or longitude is None:
                return {"status": "error", "data": {"error": "latitude and longitude required for timezone."}, "timestamp": _ts()}
            ts = int(time.time())
            params = {"location": f"{latitude},{longitude}", "timestamp": ts, "key": key, "language": language}
            resp = requests.get("https://maps.googleapis.com/maps/api/timezone/json", params=params, timeout=10)
            resp.raise_for_status()
            body = resp.json()
            if body.get("status") != "OK":
                return {"status": "error", "data": {"error": body.get("status"), "message": body.get("errorMessage", "")}, "timestamp": _ts()}
            data = {
                "timezone_id": body.get("timeZoneId"),
                "timezone_name": body.get("timeZoneName"),
                "utc_offset_hours": body.get("rawOffset", 0) / 3600,
                "dst_offset_hours": body.get("dstOffset", 0) / 3600,
                "geospatial_context": (
                    f"Timezone {body.get('timeZoneName')} ({body.get('timeZoneId')}) "
                    "identified. Critical for settlement cutoff times and market hours alignment."
                )
            }
            return {"status": "ok", "data": data, "timestamp": _ts()}

        return {"status": "error", "data": {"error": f"Unknown action: {action}"}, "timestamp": _ts()}

    except Exception as exc:
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": _ts()}
