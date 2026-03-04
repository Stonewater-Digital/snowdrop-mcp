"""
Executive Summary
-----------------
Creates Firebase Dynamic Links (short URLs) that intelligently route users to
the correct app or web destination based on their platform (Android, iOS, or
web). Uses the Firebase Dynamic Links REST API v1 with the project's Web API
Key (not a service account). Returns the generated short link and its preview
link for inspection.

Credentials:
  FIREBASE_WEB_API_KEY — Firebase Web API Key from Project Settings → General.
  This skill does NOT use service account credentials; the Dynamic Links API
  requires the Web API Key as a query parameter.

Inputs:
  long_url           : str  — The full destination URL to shorten (required)
  domain_uri_prefix  : str  — Your Dynamic Links domain (e.g. "https://example.page.link") (required)
  android_package_name : str | None  — Android package name for app routing
  ios_bundle_id        : str | None  — iOS bundle ID for app routing
  suffix_option        : str  — "SHORT" | "UNGUESSABLE" (default "SHORT")

Outputs:
  {"status": "ok"|"error", "data": {...}, "timestamp": "<ISO8601>"}

MCP Tool Name: firebase_dynamic_links_create

Agent Notes (Claude Code / Cursor / Codex CLI / Gemini CLI):
  - Set FIREBASE_WEB_API_KEY in your environment (not GOOGLE_SERVICE_ACCOUNT_JSON)
  - domain_uri_prefix must be a registered Dynamic Links domain for the project
  - SHORT produces a 4-character suffix; UNGUESSABLE produces a 17-character suffix
  - The Dynamic Links API may be deprecated in future Firebase releases; use with care
"""

import json
import logging
import os
from datetime import datetime, timezone

import requests

logger = logging.getLogger("snowdrop.firebase_dynamic_links_create")

TOOL_META = {
    "name": "firebase_dynamic_links_create",
    "description": (
        "Create a Firebase Dynamic Link (short URL) that routes users to the correct "
        "app or web destination based on their platform. "
        "Returns the short link and preview link."
    ),
    "tier": "free",
}

_DYNAMIC_LINKS_URL = "https://firebasedynamiclinks.googleapis.com/v1/shortLinks"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _wrap(status: str, data: dict) -> dict:
    return {"status": status, "data": data, "timestamp": _now()}


def firebase_dynamic_links_create(
    long_url: str,
    domain_uri_prefix: str,
    android_package_name: str | None = None,
    ios_bundle_id: str | None = None,
    suffix_option: str = "SHORT",
) -> dict:
    """Create a Firebase Dynamic Link that intelligently routes by platform.

    Args:
        long_url: The full destination URL that the Dynamic Link should resolve
            to when opened in a browser or unrecognised platform.
            Example: "https://www.example.com/products/widget-pro"
        domain_uri_prefix: Your Firebase Dynamic Links domain prefix, registered
            in the Firebase Console under Dynamic Links.
            Example: "https://example.page.link"
        android_package_name: Android application package name. When provided,
            the Dynamic Link will open the app on Android or redirect to the
            Play Store if not installed.
            Example: "com.example.myapp"
        ios_bundle_id: iOS application bundle identifier. When provided, the
            Dynamic Link will open the app on iOS or redirect to the App Store
            if not installed.
            Example: "com.example.myapp"
        suffix_option: Controls the length and format of the generated short
            code. One of "SHORT" (4 characters) or "UNGUESSABLE" (17-character
            random string). Defaults to "SHORT".

    Returns:
        dict: Standard Snowdrop envelope::

            {
                "status": "ok",
                "data": {
                    "short_link": str,
                    "preview_link": str,
                    "long_url": str,
                    "domain_uri_prefix": str
                },
                "timestamp": "<ISO8601>"
            }

    Raises:
        EnvironmentError: If FIREBASE_WEB_API_KEY is not set.
        requests.HTTPError: If the Dynamic Links API returns a non-2xx response.

    Example:
        >>> result = firebase_dynamic_links_create(
        ...     long_url="https://example.com/promo",
        ...     domain_uri_prefix="https://myapp.page.link",
        ...     android_package_name="com.example.myapp",
        ...     ios_bundle_id="com.example.myapp",
        ... )
        >>> print(result["data"]["short_link"])
        https://myapp.page.link/xY3z
    """
    logger.info(
        "firebase_dynamic_links_create called: domain=%s, suffix=%s",
        domain_uri_prefix,
        suffix_option,
    )

    api_key = os.environ.get("FIREBASE_WEB_API_KEY", "")
    if not api_key:
        return _wrap(
            "error",
            {
                "message": (
                    "FIREBASE_WEB_API_KEY environment variable is not set. "
                    "Find it in Firebase Console → Project Settings → General → Web API Key."
                )
            },
        )

    if not long_url:
        return _wrap("error", {"message": "long_url is required."})

    if not domain_uri_prefix:
        return _wrap("error", {"message": "domain_uri_prefix is required."})

    suffix_option = suffix_option.upper()
    if suffix_option not in ("SHORT", "UNGUESSABLE"):
        suffix_option = "SHORT"

    # Build the Dynamic Link info payload.
    dynamic_link_info: dict[str, object] = {
        "domainUriPrefix": domain_uri_prefix,
        "link": long_url,
    }

    if android_package_name:
        dynamic_link_info["androidInfo"] = {"androidPackageName": android_package_name}

    if ios_bundle_id:
        dynamic_link_info["iosInfo"] = {"iosBundleId": ios_bundle_id}

    payload: dict[str, object] = {
        "dynamicLinkInfo": dynamic_link_info,
        "suffix": {"option": suffix_option},
    }

    url = f"{_DYNAMIC_LINKS_URL}?key={api_key}"

    try:
        resp = requests.post(
            url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30,
        )
        resp.raise_for_status()
        body = resp.json()

        short_link = body.get("shortLink", "")
        preview_link = body.get("previewLink", "")

        logger.info(
            "firebase_dynamic_links_create succeeded: short_link=%s",
            short_link,
        )
        return _wrap(
            "ok",
            {
                "short_link": short_link,
                "preview_link": preview_link,
                "long_url": long_url,
                "domain_uri_prefix": domain_uri_prefix,
            },
        )

    except requests.HTTPError as exc:
        status_code = exc.response.status_code if exc.response is not None else 0
        error_body: str = ""
        try:
            error_body = exc.response.json().get("error", {}).get("message", "")
        except Exception:
            pass
        logger.error(
            "Firebase Dynamic Links API HTTP error %d: %s %s",
            status_code,
            exc,
            error_body,
        )
        return _wrap(
            "error",
            {
                "message": error_body or str(exc),
                "http_status": status_code,
            },
        )
    except Exception as exc:
        logger.exception("Unexpected error in firebase_dynamic_links_create")
        return _wrap("error", {"message": str(exc)})
