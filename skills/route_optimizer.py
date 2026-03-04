"""
Executive Summary:
    Google Route Optimization API skill for logistics, delivery sequencing, and travel
    analysis. Supports full fleet-level tour optimization via the Route Optimization API
    (SA credentials), point-to-point directions, and multi-origin distance matrices via
    the Maps APIs. Designed for real estate site visits, fund asset inspections, and
    any multi-stop logistics workflow within Snowdrop Core.

Inputs:
    action         (str, required)        — "optimize" | "directions" | "distance_matrix"
    origin         (str)                  — Starting address or "lat,lng" (directions)
    destination    (str)                  — Ending address or "lat,lng" (directions)
    waypoints      (list[str])            — Intermediate stops (directions, max 25)
    vehicles       (list[dict])           — Fleet vehicles with location and cost (optimize)
    shipments      (list[dict])           — Pickup/delivery tasks with load demands (optimize)
    departure_time (str, ISO8601)         — Departure time for traffic-aware routing
    mode           (str, default "driving") — "driving" | "walking" | "transit"
    avoid          (list[str])            — Features to avoid: "tolls", "highways", "ferries"
    project_id     (str)                  — GCP project; falls back to GOOGLE_PROJECT_ID env

Outputs:
    {"status": "ok"|"error", "data": {route/optimization details}, "timestamp": ISO8601}

MCP Tool Name: route_optimizer

Agent Notes:
    - optimize uses SA Bearer token (GOOGLE_SERVICE_ACCOUNT_JSON → GCP_SERVICE_ACCOUNT_FILE)
    - directions and distance_matrix use GOOGLE_MAPS_API_KEY only
    - All distances returned in km, durations in minutes for human readability
    - optimize returns vehicle_routes with stop sequences and estimated cost per vehicle
    - distance_matrix supports pipe-delimited multi-origin/destination strings
"""

import json
import os
from datetime import datetime, timezone

import requests

TOOL_META = {
    "name": "route_optimizer",
    "description": (
        "Google Route Optimization API skill for fleet tour optimization, point-to-point "
        "directions, and distance matrix calculations. Supports real estate inspections, "
        "logistics planning, and multi-stop delivery sequencing."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": ["optimize", "directions", "distance_matrix"],
                "description": "The routing operation to perform."
            },
            "origin": {"type": "string", "description": "Start address or 'lat,lng' string."},
            "destination": {"type": "string", "description": "End address or 'lat,lng' string."},
            "waypoints": {
                "type": "array", "items": {"type": "string"},
                "description": "Intermediate stops for directions (max 25)."
            },
            "vehicles": {
                "type": "array", "items": {"type": "object"},
                "description": "Fleet vehicles with start_location, end_location, cost_per_hour."
            },
            "shipments": {
                "type": "array", "items": {"type": "object"},
                "description": "Pickup/delivery tasks with arrival_location and load_demands."
            },
            "departure_time": {
                "type": "string", "format": "date-time",
                "description": "ISO8601 departure time for traffic-aware routing."
            },
            "mode": {
                "type": "string", "default": "driving",
                "enum": ["driving", "walking", "transit"],
                "description": "Travel mode for directions and distance_matrix."
            },
            "avoid": {
                "type": "array", "items": {"type": "string"},
                "description": "Route features to avoid: tolls, highways, ferries."
            },
            "project_id": {
                "type": "string",
                "description": "GCP project ID. Falls back to GOOGLE_PROJECT_ID env var."
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
    return datetime.now(timezone.utc).isoformat()


def _maps_api_key() -> str:
    key = os.environ.get("GOOGLE_MAPS_API_KEY")
    if not key:
        raise EnvironmentError("GOOGLE_MAPS_API_KEY environment variable is not set.")
    return key


def _sa_bearer_token() -> str:
    """Obtain a short-lived Bearer token from SA credentials for Route Optimization API."""
    import google.auth.transport.requests
    from google.oauth2 import service_account

    scopes = ["https://www.googleapis.com/auth/cloud-platform"]
    sa_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
    if sa_json:
        info = json.loads(sa_json)
        creds = service_account.Credentials.from_service_account_info(info, scopes=scopes)
    else:
        sa_file = os.environ.get("GCP_SERVICE_ACCOUNT_FILE")
        if not sa_file:
            raise EnvironmentError(
                "No GCP credentials. Set GOOGLE_SERVICE_ACCOUNT_JSON or GCP_SERVICE_ACCOUNT_FILE."
            )
        creds = service_account.Credentials.from_service_account_file(sa_file, scopes=scopes)
    creds.refresh(google.auth.transport.requests.Request())
    return creds.token


def _meters_to_km(meters: int) -> float:
    return round(meters / 1000, 3)


def _seconds_to_min(seconds: int) -> float:
    return round(seconds / 60, 1)


def route_optimizer(
    action: str,
    origin: str = None,
    destination: str = None,
    waypoints: list = None,
    vehicles: list = None,
    shipments: list = None,
    departure_time: str = None,
    mode: str = "driving",
    avoid: list = None,
    project_id: str = None
) -> dict:
    """Execute a Google routing operation: tour optimization, directions, or distance matrix."""
    try:
        if action == "optimize":
            project = project_id or os.environ.get("GOOGLE_PROJECT_ID")
            if not project:
                return {"status": "error", "data": {"error": "project_id required (or set GOOGLE_PROJECT_ID)."}, "timestamp": _ts()}
            if not vehicles or not shipments:
                return {"status": "error", "data": {"error": "vehicles and shipments are required for optimize."}, "timestamp": _ts()}

            token = _sa_bearer_token()
            url = f"https://routeoptimization.googleapis.com/v1/projects/{project}:optimizeTours"
            headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
            payload = {"model": {"vehicles": vehicles, "shipments": shipments}}
            if departure_time:
                payload["model"]["globalStartTime"] = departure_time

            resp = requests.post(url, json=payload, headers=headers, timeout=60)
            resp.raise_for_status()
            body = resp.json()

            vehicle_routes = []
            for idx, vr in enumerate(body.get("routes", [])):
                visits = []
                for visit in vr.get("visits", []):
                    visits.append({
                        "shipment_index": visit.get("shipmentIndex"),
                        "is_pickup": visit.get("isPickup", True),
                        "start_time": visit.get("startTime"),
                        "detour": visit.get("detour")
                    })
                metrics = vr.get("metrics", {})
                vehicle_routes.append({
                    "vehicle_index": idx,
                    "stops": visits,
                    "total_duration_min": _seconds_to_min(
                        int(metrics.get("totalDuration", "0s").rstrip("s") or 0)
                    ),
                    "travel_duration_min": _seconds_to_min(
                        int(metrics.get("travelDuration", "0s").rstrip("s") or 0)
                    ),
                    "total_distance_km": _meters_to_km(
                        int(metrics.get("travelDistanceMeters", 0))
                    )
                })

            return {
                "status": "ok",
                "data": {
                    "vehicle_routes": vehicle_routes,
                    "total_vehicles_used": len(vehicle_routes),
                    "skipped_shipments": body.get("skippedShipments", [])
                },
                "timestamp": _ts()
            }

        if action == "directions":
            if not origin or not destination:
                return {"status": "error", "data": {"error": "origin and destination required for directions."}, "timestamp": _ts()}
            key = _maps_api_key()
            params = {
                "origin": origin, "destination": destination,
                "mode": mode, "language": "en", "key": key
            }
            if waypoints:
                params["waypoints"] = "|".join(waypoints)
            if avoid:
                params["avoid"] = "|".join(avoid)
            if departure_time:
                import calendar
                dt = datetime.fromisoformat(departure_time.replace("Z", "+00:00"))
                params["departure_time"] = calendar.timegm(dt.timetuple())

            resp = requests.get("https://maps.googleapis.com/maps/api/directions/json", params=params, timeout=15)
            resp.raise_for_status()
            body = resp.json()
            if body.get("status") != "OK":
                return {"status": "error", "data": {"error": body.get("status"), "message": body.get("error_message", "")}, "timestamp": _ts()}

            route = body["routes"][0]
            legs_out = []
            total_dist = 0
            total_dur = 0
            for leg in route.get("legs", []):
                dist_m = leg["distance"]["value"]
                dur_s = leg["duration"]["value"]
                total_dist += dist_m
                total_dur += dur_s
                legs_out.append({
                    "start_address": leg["start_address"],
                    "end_address": leg["end_address"],
                    "distance_km": _meters_to_km(dist_m),
                    "duration_min": _seconds_to_min(dur_s),
                    "steps": len(leg.get("steps", []))
                })

            return {
                "status": "ok",
                "data": {
                    "total_distance_km": _meters_to_km(total_dist),
                    "total_duration_min": _seconds_to_min(total_dur),
                    "legs": legs_out,
                    "summary": route.get("summary"),
                    "warnings": route.get("warnings", []),
                    "waypoint_order": route.get("waypoint_order", [])
                },
                "timestamp": _ts()
            }

        if action == "distance_matrix":
            if not origin or not destination:
                return {"status": "error", "data": {"error": "origin and destination required for distance_matrix."}, "timestamp": _ts()}
            key = _maps_api_key()
            params = {
                "origins": origin, "destinations": destination,
                "mode": mode, "language": "en", "key": key
            }
            if avoid:
                params["avoid"] = "|".join(avoid)

            resp = requests.get("https://maps.googleapis.com/maps/api/distancematrix/json", params=params, timeout=15)
            resp.raise_for_status()
            body = resp.json()
            if body.get("status") != "OK":
                return {"status": "error", "data": {"error": body.get("status")}, "timestamp": _ts()}

            rows_out = []
            for orig_addr, row in zip(body.get("origin_addresses", []), body.get("rows", [])):
                elements_out = []
                for dest_addr, el in zip(body.get("destination_addresses", []), row.get("elements", [])):
                    if el.get("status") == "OK":
                        elements_out.append({
                            "destination": dest_addr,
                            "distance_km": _meters_to_km(el["distance"]["value"]),
                            "duration_min": _seconds_to_min(el["duration"]["value"]),
                            "status": "ok"
                        })
                    else:
                        elements_out.append({"destination": dest_addr, "status": el.get("status", "error")})
                rows_out.append({"origin": orig_addr, "destinations": elements_out})

            return {
                "status": "ok",
                "data": {
                    "matrix": rows_out,
                    "origin_count": len(body.get("origin_addresses", [])),
                    "destination_count": len(body.get("destination_addresses", []))
                },
                "timestamp": _ts()
            }

        return {"status": "error", "data": {"error": f"Unknown action: {action}"}, "timestamp": _ts()}

    except Exception as exc:
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": _ts()}
