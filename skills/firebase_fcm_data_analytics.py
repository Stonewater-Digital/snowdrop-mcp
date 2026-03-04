"""
Executive Summary
-----------------
Retrieves Firebase Cloud Messaging (FCM) delivery analytics from the FCM Data API
(v1beta1). Reports message send counts, delivery rates, and outcome breakdowns
(accepted, delivered, delivery_failed, pending, skipped) for a specified date range.
Optionally filters by Firebase app ID. Covers Android delivery data; iOS and Web
analytics require separate endpoints.

Credentials resolved ADC-first (Cloud Run), then GOOGLE_SERVICE_ACCOUNT_JSON (local dev).

Inputs:
  project_id : str | None — GCP project ID (falls back to GOOGLE_PROJECT_ID env)
  start_date : str        — start of date range in "YYYY-MM-DD" format (required)
  end_date   : str        — end of date range in "YYYY-MM-DD" format (required)
  app_id     : str | None — Firebase app ID filter (e.g. "1:123456:android:abc")

Outputs:
  {"status": "ok"|"error", "data": {...}, "timestamp": "<ISO8601>"}

MCP Tool Name: firebase_fcm_data_analytics

Agent Notes:
  - Required IAM: roles/firebase.viewer or roles/firebaseanalytics.viewer
  - The FCM Data API currently supports Android delivery data via androidDeliveryData.
  - Data is typically available with a 24–48 hour delay.
  - message_insight_percent_estimated fields are included when the API returns them
    (available for large message volumes only).
  - Dates must be in "YYYY-MM-DD" format; the API uses a structured date object.
"""

import json
import logging
import os
from datetime import datetime, timezone

import requests

logger = logging.getLogger("snowdrop.firebase_fcm_data_analytics")

TOOL_META = {
    "name": "firebase_fcm_data_analytics",
    "description": (
        "Get Firebase Cloud Messaging delivery analytics data — "
        "send counts, delivery rates, and open rates for a date range."
    ),
    "tier": "free",
}

_CLOUD_PLATFORM_SCOPE = "https://www.googleapis.com/auth/cloud-platform"


def _get_access_token(scopes: list[str]) -> str:
    """Get an OAuth2 access token. ADC-first (Cloud Run), JSON fallback (local dev).

    Args:
        scopes: List of OAuth2 scope strings to request.

    Returns:
        A valid Bearer token string.

    Raises:
        RuntimeError: If no credential source is available.
    """
    import google.auth.transport.requests

    sa_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
    if sa_json:
        from google.oauth2 import service_account
        creds = service_account.Credentials.from_service_account_info(
            json.loads(sa_json), scopes=scopes
        )
    else:
        import google.auth
        creds, _ = google.auth.default(scopes=scopes)
    creds.refresh(google.auth.transport.requests.Request())
    return creds.token


def _now() -> str:
    """Return current UTC time as ISO 8601 string."""
    return datetime.now(timezone.utc).isoformat()


def _parse_date(date_str: str) -> dict:
    """Parse a "YYYY-MM-DD" string into a FCM Data API structured date dict.

    Args:
        date_str: Date string in "YYYY-MM-DD" format.

    Returns:
        Dict with ``year`` (int), ``month`` (int), ``day`` (int) keys.

    Raises:
        ValueError: If the string does not match the expected format.
    """
    parsed = datetime.strptime(date_str, "%Y-%m-%d")
    return {"year": parsed.year, "month": parsed.month, "day": parsed.day}


def _normalize_entry(raw: dict) -> dict:
    """Normalize a raw FCM delivery data entry into a flat summary dict.

    Args:
        raw: A single androidDeliveryData entry from the FCM Data API response.

    Returns:
        Normalized dict with date, app_id, message_outcome_counts, and
        message_insight_percent_estimated fields.
    """
    # Date may be in structured { year, month, day } format
    raw_date = raw.get("date", {})
    if isinstance(raw_date, dict):
        year = raw_date.get("year", 0)
        month = raw_date.get("month", 0)
        day = raw_date.get("day", 0)
        date_str = f"{year:04d}-{month:02d}-{day:02d}"
    else:
        date_str = str(raw_date)

    # Outcome counts live under messageOutcomeStats or messageOutcomeCounts
    outcome_raw = raw.get("messageOutcomeStats", raw.get("messageOutcomeCounts", {}))
    outcome_counts: dict = {
        "accepted": int(outcome_raw.get("accepted", 0)),
        "delivered": int(outcome_raw.get("delivered", 0)),
        "delivery_failed": int(outcome_raw.get("deliveryFailed", outcome_raw.get("delivery_failed", 0))),
        "pending": int(outcome_raw.get("pending", 0)),
        "skipped": int(outcome_raw.get("skipped", 0)),
        "collapsed": int(outcome_raw.get("collapsed", 0)),
    }

    # Insight percentages (only available for high-volume campaigns)
    insight_raw = raw.get("messageInsightStats", raw.get("messageInsightPercents", {}))
    insight_percent: dict = {}
    if insight_raw:
        insight_percent = {
            "priority_lowered": insight_raw.get("priorityLowered", insight_raw.get("priority_lowered", None)),
        }
        # Remove None values to keep output clean
        insight_percent = {k: v for k, v in insight_percent.items() if v is not None}

    return {
        "date": date_str,
        "app_id": raw.get("appId", raw.get("app_id", "")),
        "analytics_label": raw.get("analyticsLabel", ""),
        "message_outcome_counts": outcome_counts,
        "message_insight_percent_estimated": insight_percent,
    }


def firebase_fcm_data_analytics(
    project_id: str | None = None,
    start_date: str = "",
    end_date: str = "",
    app_id: str | None = None,
) -> dict:
    """Retrieve Firebase Cloud Messaging delivery analytics for a date range.

    Queries the FCM Data API (v1beta1) ``androidDeliveryData`` endpoint for
    message outcome statistics across the specified date range. Results are
    grouped by date and, when ``app_id`` is provided, filtered to that
    specific Firebase application.

    Args:
        project_id: GCP project ID. Defaults to the ``GOOGLE_PROJECT_ID``
            environment variable when not provided.
        start_date: Start of the reporting date range in ``"YYYY-MM-DD"``
            format. Required.
        end_date: End of the reporting date range in ``"YYYY-MM-DD"``
            format. Required.
        app_id: Optional Firebase app ID to narrow results to a single app
            (e.g. ``"1:123456789:android:abcdef0123456789"``).

    Returns:
        dict with keys:
            - status (str): ``"ok"`` or ``"error"``.
            - data (dict): Contains ``entries`` (list of normalized delivery
              data records), ``count`` (int), ``start_date`` (str),
              ``end_date`` (str), ``app_id`` (str | None), and
              ``project_id`` (str).
            - timestamp (str): ISO 8601 UTC execution timestamp.

    Raises:
        Does not raise; all exceptions are caught and returned as error dicts.

    Example:
        >>> result = firebase_fcm_data_analytics(
        ...     project_id="my-gcp-project",
        ...     start_date="2026-02-01",
        ...     end_date="2026-02-22",
        ... )
        >>> result["status"]
        'ok'
        >>> isinstance(result["data"]["entries"], list)
        True
    """
    logger.info(
        "firebase_fcm_data_analytics: entry project=%s start=%s end=%s app_id=%s",
        project_id,
        start_date,
        end_date,
        app_id,
    )

    project_id = project_id or os.environ.get("GOOGLE_PROJECT_ID", "")
    if not project_id:
        logger.error("firebase_fcm_data_analytics: project_id missing")
        return {
            "status": "error",
            "data": {"message": "project_id is required or set GOOGLE_PROJECT_ID"},
            "timestamp": _now(),
        }

    if not start_date or not end_date:
        logger.error("firebase_fcm_data_analytics: start_date and end_date are required")
        return {
            "status": "error",
            "data": {"message": "start_date and end_date are required in YYYY-MM-DD format"},
            "timestamp": _now(),
        }

    try:
        start_struct = _parse_date(start_date)
        end_struct = _parse_date(end_date)
    except ValueError as exc:
        logger.error("firebase_fcm_data_analytics: date parse error: %s", exc)
        return {
            "status": "error",
            "data": {"message": f"Invalid date format: {exc}. Use YYYY-MM-DD."},
            "timestamp": _now(),
        }

    try:
        token = _get_access_token([_CLOUD_PLATFORM_SCOPE])
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        # Build request body with date range filter
        request_body: dict = {
            "dateRange": {
                "startDate": start_struct,
                "endDate": end_struct,
            }
        }

        if app_id:
            request_body["appId"] = app_id

        # Primary endpoint: androidDeliveryData
        primary_url = (
            f"https://fcmdata.googleapis.com/v1beta1"
            f"/projects/{project_id}/androidDeliveryData:list"
        )

        logger.info("firebase_fcm_data_analytics: POST %s", primary_url)
        resp = requests.post(
            primary_url, headers=headers, json=request_body, timeout=30
        )

        entries_raw: list[dict] = []
        source: str

        if resp.status_code == 200:
            body = resp.json()
            entries_raw = body.get("androidDeliveryData", body.get("deliveryData", []))
            source = "androidDeliveryData"
            logger.info(
                "firebase_fcm_data_analytics: primary endpoint returned %d entries",
                len(entries_raw),
            )
        else:
            logger.warning(
                "firebase_fcm_data_analytics: primary endpoint returned %d — trying deliveryData fallback",
                resp.status_code,
            )

            # Fallback: generic deliveryData endpoint
            fallback_url = (
                f"https://fcmdata.googleapis.com/v1beta1"
                f"/projects/{project_id}/deliveryData"
            )
            params: dict = {}
            if app_id:
                params["appId"] = app_id

            logger.info("firebase_fcm_data_analytics: GET %s", fallback_url)
            fb_resp = requests.get(
                fallback_url, headers=headers, params=params, timeout=30
            )

            if fb_resp.status_code != 200:
                logger.error(
                    "firebase_fcm_data_analytics: both endpoints failed: %d / %d",
                    resp.status_code,
                    fb_resp.status_code,
                )
                return {
                    "status": "error",
                    "data": {
                        "message": (
                            f"androidDeliveryData: {resp.status_code}; "
                            f"deliveryData fallback: {fb_resp.status_code}"
                        ),
                        "primary_response": resp.text[:300],
                        "fallback_response": fb_resp.text[:300],
                    },
                    "timestamp": _now(),
                }

            body = fb_resp.json()
            entries_raw = body.get("deliveryData", body.get("androidDeliveryData", []))
            source = "deliveryData_fallback"
            logger.info(
                "firebase_fcm_data_analytics: fallback returned %d entries",
                len(entries_raw),
            )

        # Filter by app_id client-side if provided (API may not support server-side filter)
        if app_id:
            entries_raw = [
                e for e in entries_raw
                if e.get("appId", e.get("app_id", "")) == app_id
            ]

        entries = [_normalize_entry(e) for e in entries_raw]

        # Compute aggregate summary
        total_accepted = sum(e["message_outcome_counts"]["accepted"] for e in entries)
        total_delivered = sum(e["message_outcome_counts"]["delivered"] for e in entries)
        total_failed = sum(e["message_outcome_counts"]["delivery_failed"] for e in entries)
        delivery_rate: float = (
            round(total_delivered / total_accepted * 100, 2)
            if total_accepted > 0
            else 0.0
        )

        logger.info(
            "firebase_fcm_data_analytics: exit success entries=%d accepted=%d delivered=%d",
            len(entries),
            total_accepted,
            total_delivered,
        )

        return {
            "status": "ok",
            "data": {
                "entries": entries,
                "count": len(entries),
                "summary": {
                    "total_accepted": total_accepted,
                    "total_delivered": total_delivered,
                    "total_delivery_failed": total_failed,
                    "delivery_rate_pct": delivery_rate,
                },
                "start_date": start_date,
                "end_date": end_date,
                "app_id": app_id,
                "source": source,
                "project_id": project_id,
            },
            "timestamp": _now(),
        }

    except Exception as exc:
        logger.error(
            "firebase_fcm_data_analytics: unexpected error: %s", exc, exc_info=True
        )
        return {
            "status": "error",
            "data": {"message": str(exc)},
            "timestamp": _now(),
        }
