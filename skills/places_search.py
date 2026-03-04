"""
Executive Summary:
    Business and real estate intelligence skill powered by the Google Places API (New).
    Supports full-text search, nearby place discovery, and detailed place lookups.
    Designed for deal sourcing, market density analysis, and real estate due diligence
    within Thunder's fund accounting and investment workflows. Includes an
    investment_signal field that provides a heuristic read on business health and
    density for a given location.

Inputs:
    action         (str, required)  — "search" | "details" | "nearby"
    query          (str)            — free-text search string (search action)
    place_id       (str)            — Google Place ID (details action)
    location       (str)            — "lat,lng" string (nearby action)
    radius_meters  (int, default 500)  — search radius for nearby action
    type           (str)            — place type filter (e.g. "bank", "restaurant")
    max_results    (int, default 10)   — maximum places to return

Outputs:
    status           (str)  — "ok" | "error"
    data             (dict) — list of places with name, address, rating,
                              price_level, business_status, location,
                              plus investment_signal summary
    timestamp        (str)  — ISO 8601 UTC

MCP Tool Name: places_search

Agent Notes:
    - Requires GOOGLE_MAPS_API_KEY with Places API (New) enabled.
    - Uses X-Goog-Api-Key header (not query param) per Places API (New) spec.
    - Field mask is sent via X-Goog-FieldMask header to control billing.
    - investment_signal is heuristic — suitable for initial screening only.
    - Place details (details action) fetches extended fields including opening
      hours and website.
    - Rate limits: Places API (New) — billed per field mask; check GCP quotas.
"""

import os
import datetime
import requests

TOOL_META = {
    "name": "places_search",
    "description": (
        "Search, discover, and retrieve details for businesses and points of interest "
        "using the Google Places API (New). Supports free-text search, nearby discovery, "
        "and full place detail lookups. Returns structured business data plus an "
        "investment_signal field assessing business density and health for real estate "
        "and market analysis."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": ["search", "details", "nearby"],
                "description": "Places operation to perform.",
            },
            "query": {
                "type": "string",
                "description": "Free-text search query (search action).",
            },
            "place_id": {
                "type": "string",
                "description": "Google Place ID for detail lookup (details action).",
            },
            "location": {
                "type": "string",
                "description": "'lat,lng' string used to bias search or anchor nearby (nearby/search actions).",
            },
            "radius_meters": {
                "type": "integer",
                "default": 500,
                "description": "Search radius in meters for nearby action.",
            },
            "type": {
                "type": "string",
                "description": "Place type filter (e.g. 'restaurant', 'bank', 'real_estate_agency').",
            },
            "max_results": {
                "type": "integer",
                "default": 10,
                "description": "Maximum number of places to return (1–20).",
            },
        },
        "required": ["action"],
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

_SEARCH_FIELD_MASK = (
    "places.id,places.displayName,places.formattedAddress,"
    "places.rating,places.userRatingCount,places.priceLevel,"
    "places.businessStatus,places.location,places.types"
)

_DETAIL_FIELD_MASK = (
    "id,displayName,formattedAddress,rating,userRatingCount,"
    "priceLevel,businessStatus,location,types,"
    "currentOpeningHours,websiteUri,nationalPhoneNumber,editorialSummary"
)


def _now_iso() -> str:
    return datetime.datetime.utcnow().isoformat() + "Z"


def _error(msg: str) -> dict:
    return {"status": "error", "data": {"message": msg}, "timestamp": _now_iso()}


def _parse_location(location_str: str) -> dict:
    """Parse 'lat,lng' string to Places API location bias dict."""
    parts = [p.strip() for p in location_str.split(",")]
    if len(parts) != 2:
        raise ValueError(f"location must be 'lat,lng' format, got: {location_str}")
    return {"latitude": float(parts[0]), "longitude": float(parts[1])}


def _normalize_place(place: dict) -> dict:
    """Normalize a Places API (New) place object to a consistent flat dict."""
    display_name = place.get("displayName", {})
    name = display_name.get("text", "") if isinstance(display_name, dict) else str(display_name)
    loc = place.get("location", {})
    return {
        "place_id": place.get("id", ""),
        "name": name,
        "address": place.get("formattedAddress", ""),
        "rating": place.get("rating"),
        "rating_count": place.get("userRatingCount"),
        "price_level": place.get("priceLevel"),
        "business_status": place.get("businessStatus", "UNKNOWN"),
        "types": place.get("types", []),
        "latitude": loc.get("latitude"),
        "longitude": loc.get("longitude"),
    }


def _investment_signal(places: list, action: str, query: str, place_type: str) -> str:
    """Heuristic investment signal based on place density, ratings, and business health."""
    if not places:
        return "No places found — possible greenfield opportunity or data gap; verify manually."

    total = len(places)
    operational = sum(1 for p in places if p.get("business_status") == "OPERATIONAL")
    closed = sum(1 for p in places if p.get("business_status") in ("CLOSED_PERMANENTLY", "CLOSED_TEMPORARILY"))
    rated = [p["rating"] for p in places if p.get("rating")]
    avg_rating = round(sum(rated) / len(rated), 2) if rated else None

    vacancy_rate = round(closed / total * 100, 1) if total else 0
    health = "strong" if vacancy_rate < 10 else "moderate" if vacancy_rate < 30 else "distressed"

    parts = [
        f"{total} places found ({operational} operational, {closed} closed/temp-closed).",
        f"Vacancy indicator: {vacancy_rate}% — market health: {health}.",
    ]
    if avg_rating:
        sentiment = "positive consumer sentiment" if avg_rating >= 4.0 else "mixed consumer sentiment" if avg_rating >= 3.0 else "negative consumer sentiment"
        parts.append(f"Avg rating {avg_rating}/5 — {sentiment}.")
    if health == "distressed":
        parts.append("High closure rate may signal economic stress or opportunity for repositioning.")
    elif health == "strong" and total >= 8:
        parts.append("Dense, healthy business cluster — supportive of retail/mixed-use real estate values.")

    return " ".join(parts)


def places_search(
    action: str,
    query: str = None,
    place_id: str = None,
    location: str = None,
    radius_meters: int = 500,
    type: str = None,
    max_results: int = 10,
) -> dict:
    api_key = os.environ.get("GOOGLE_MAPS_API_KEY")
    if not api_key:
        return _error("GOOGLE_MAPS_API_KEY environment variable is not set.")

    max_results = max(1, min(max_results, 20))
    headers = {
        "X-Goog-Api-Key": api_key,
        "Content-Type": "application/json",
    }

    try:
        if action == "search":
            if not query:
                return _error("'query' parameter is required for action 'search'.")

            headers["X-Goog-FieldMask"] = _SEARCH_FIELD_MASK
            body = {"textQuery": query, "maxResultCount": max_results}

            if location:
                coords = _parse_location(location)
                body["locationBias"] = {
                    "circle": {
                        "center": coords,
                        "radius": float(radius_meters),
                    }
                }
            if type:
                body["includedType"] = type

            resp = requests.post(
                "https://places.googleapis.com/v1/places:searchText",
                headers=headers,
                json=body,
                timeout=15,
            )
            resp.raise_for_status()
            raw_places = resp.json().get("places", [])
            normalized = [_normalize_place(p) for p in raw_places]

            return {
                "status": "ok",
                "data": {
                    "action": "search",
                    "query": query,
                    "count": len(normalized),
                    "places": normalized,
                    "investment_signal": _investment_signal(normalized, action, query, type or ""),
                },
                "timestamp": _now_iso(),
            }

        elif action == "nearby":
            if not location:
                return _error("'location' parameter (lat,lng) is required for action 'nearby'.")

            coords = _parse_location(location)
            headers["X-Goog-FieldMask"] = _SEARCH_FIELD_MASK
            body = {
                "locationRestriction": {
                    "circle": {
                        "center": coords,
                        "radius": float(radius_meters),
                    }
                },
                "maxResultCount": max_results,
            }
            if type:
                body["includedTypes"] = [type]

            resp = requests.post(
                "https://places.googleapis.com/v1/places:searchNearby",
                headers=headers,
                json=body,
                timeout=15,
            )
            resp.raise_for_status()
            raw_places = resp.json().get("places", [])
            normalized = [_normalize_place(p) for p in raw_places]

            return {
                "status": "ok",
                "data": {
                    "action": "nearby",
                    "center": coords,
                    "radius_meters": radius_meters,
                    "count": len(normalized),
                    "places": normalized,
                    "investment_signal": _investment_signal(normalized, action, "", type or ""),
                },
                "timestamp": _now_iso(),
            }

        elif action == "details":
            if not place_id:
                return _error("'place_id' parameter is required for action 'details'.")

            headers["X-Goog-FieldMask"] = _DETAIL_FIELD_MASK
            resp = requests.get(
                f"https://places.googleapis.com/v1/places/{place_id}",
                headers=headers,
                timeout=15,
            )
            resp.raise_for_status()
            place = resp.json()
            normalized = _normalize_place(place)

            editorial = place.get("editorialSummary", {})
            normalized["editorial_summary"] = editorial.get("text", "") if isinstance(editorial, dict) else ""
            normalized["website"] = place.get("websiteUri", "")
            normalized["phone"] = place.get("nationalPhoneNumber", "")
            hours = place.get("currentOpeningHours", {})
            normalized["open_now"] = hours.get("openNow") if isinstance(hours, dict) else None
            normalized["weekday_descriptions"] = hours.get("weekdayDescriptions", []) if isinstance(hours, dict) else []

            signal = _investment_signal([normalized], action, "", "")
            return {
                "status": "ok",
                "data": {
                    "action": "details",
                    "place": normalized,
                    "investment_signal": signal,
                },
                "timestamp": _now_iso(),
            }

        else:
            return _error(f"Unknown action '{action}'. Must be 'search', 'details', or 'nearby'.")

    except ValueError as exc:
        return _error(f"Parameter error: {exc}")
    except requests.HTTPError as exc:
        return _error(f"Google Places API HTTP error: {exc.response.status_code} — {exc.response.text[:300]}")
    except requests.RequestException as exc:
        return _error(f"Network error contacting Google Places API: {exc}")
    except Exception as exc:
        return _error(f"Unexpected error in places_search: {exc}")
