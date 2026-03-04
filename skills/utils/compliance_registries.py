"""Shared regulator registry utilities for compliance skills.

Centralises ASIC/FCA/ESMA/CBI/AMF/SEC/FINRA lookups so skills stop owning
their own scraping logic. Supports HTTP-backed lookups when environment
variables are configured, but always falls back to deterministic sample data
so offline testing and reasoning remain possible.
"""
from __future__ import annotations

import os
import time
from typing import Any, Callable, TypedDict

import requests

from .logging import log_lesson
from .time import get_iso_timestamp


class RegistryRecord(TypedDict, total=False):
    """Normalised registry entity payload."""

    registry: str
    identifier: str
    entity_name: str
    status: str
    jurisdiction: str
    last_updated: str
    permissions: list[str]
    metadata: dict[str, Any]


_REGISTRY_TTL_SECONDS = 6 * 3600
_REGISTRY_CACHE: dict[tuple[str, str], tuple[float, RegistryRecord]] = {}


_REGISTRY_HTTP_CONFIG: dict[str, dict[str, Any]] = {
    "asic": {
        "record_url_env": "ASIC_CONNECT_API_URL",
        "search_url_env": "ASIC_CONNECT_SEARCH_URL",
        "token_env": "ASIC_CONNECT_TOKEN",
        "session_env": "ASIC_CONNECT_SESSION",
        "identifier_param": "licenseNumber",
        "query_param": "query",
    },
    "fca": {
        "record_url_env": "FCA_REGISTER_API_URL",
        "search_url_env": "FCA_REGISTER_SEARCH_URL",
        "token_env": "FCA_REGISTER_API_KEY",
        "identifier_param": "firmReferenceNumber",
        "query_param": "q",
    },
    "esma": {
        "record_url_env": "ESMA_REGISTER_API_URL",
        "search_url_env": "ESMA_REGISTER_SEARCH_URL",
        "token_env": "ESMA_REGISTER_API_KEY",
        "identifier_param": "entityId",
        "query_param": "q",
    },
    "cbi": {
        "record_url_env": "CBI_ONR_API_URL",
        "search_url_env": "CBI_ONR_SEARCH_URL",
        "token_env": "CBI_ONR_API_TOKEN",
        "identifier_param": "onrId",
        "query_param": "name",
    },
    "amf": {
        "record_url_env": "AMF_ICO_API_URL",
        "search_url_env": "AMF_ICO_SEARCH_URL",
        "token_env": "AMF_ICO_API_TOKEN",
        "identifier_param": "visaNumber",
        "query_param": "project",
    },
    "sec": {
        "record_url_env": "SEC_IAPD_API_URL",
        "search_url_env": "SEC_IAPD_SEARCH_URL",
        "token_env": "SEC_IAPD_API_KEY",
        "identifier_param": "crd",
        "query_param": "firm",
    },
    "finra": {
        "record_url_env": "FINRA_BROKER_API_URL",
        "search_url_env": "FINRA_BROKER_SEARCH_URL",
        "token_env": "FINRA_BROKER_API_KEY",
        "identifier_param": "crd",
        "query_param": "name",
    },
    "jfsa": {
        "record_url_env": "JFSA_CAESP_API_URL",
        "search_url_env": "JFSA_CAESP_SEARCH_URL",
        "token_env": "JFSA_CAESP_API_TOKEN",
        "identifier_param": "registrationId",
        "query_param": "entity",
    },
    "nsdl": {
        "record_url_env": "NSDL_REGISTRY_API_URL",
        "search_url_env": "NSDL_REGISTRY_SEARCH_URL",
        "token_env": "NSDL_API_KEY",
        "identifier_param": "registrationId",
        "query_param": "name",
    },
    "cdsl": {
        "record_url_env": "CDSL_REGISTRY_API_URL",
        "search_url_env": "CDSL_REGISTRY_SEARCH_URL",
        "token_env": "CDSL_API_KEY",
        "identifier_param": "registrationId",
        "query_param": "name",
    },
}


_SAMPLE_REGISTRY_DATA: dict[str, list[RegistryRecord]] = {
    "asic": [
        {
            "registry": "asic",
            "identifier": "001234567",
            "entity_name": "Stonewater Capital Pty Ltd",
            "status": "ACTIVE",
            "jurisdiction": "AU",
            "last_updated": "2026-02-18T00:00:00Z",
            "permissions": [
                "Dealing in securities",
                "Advising on derivatives",
                "Custody services",
            ],
            "metadata": {"afsl_number": "001234567", "relief": ["s911a(2)(h)"]},
        },
        {
            "registry": "asic",
            "identifier": "453211",
            "entity_name": "Northern Hemisphere Asset Management",
            "status": "SUSPENDED",
            "jurisdiction": "AU",
            "last_updated": "2026-01-31T00:00:00Z",
            "permissions": ["Advising on securities"],
            "metadata": {"suspension_reason": "Late AFSL fee"},
        },
    ],
    "fca": [
        {
            "registry": "fca",
            "identifier": "765432",
            "entity_name": "Stonewater Capital UK Limited",
            "status": "AUTHORISED",
            "jurisdiction": "GB",
            "last_updated": "2026-02-12T00:00:00Z",
            "permissions": ["MiFID investment firm", "CASS medium"],
            "metadata": {"passporting": False},
        }
    ],
    "esma": [
        {
            "registry": "esma",
            "identifier": "EU-ICR-90876",
            "entity_name": "Stonewater EU ICAV",
            "status": "NOTIFIED",
            "jurisdiction": "IE",
            "last_updated": "2026-02-20T00:00:00Z",
            "permissions": ["UCITS management company"],
            "metadata": {"host_states": ["FR", "DE", "ES"]},
        }
    ],
    "cbi": [
        {
            "registry": "cbi",
            "identifier": "ONR-778899",
            "entity_name": "Stonewater ICAV",
            "status": "AUTHORISED",
            "jurisdiction": "IE",
            "last_updated": "2026-02-10T00:00:00Z",
            "permissions": ["QIAIF umbrella"],
            "metadata": {"last_return": "2025-12-31"},
        }
    ],
    "amf": [
        {
            "registry": "amf",
            "identifier": "ICO-2025-042",
            "entity_name": "Stonewater Token Visa",
            "status": "VISA_GRANTED",
            "jurisdiction": "FR",
            "last_updated": "2025-11-05T00:00:00Z",
            "permissions": ["Token offering visa"],
            "metadata": {"visa_valid_until": "2026-11-05"},
        }
    ],
    "sec": [
        {
            "registry": "sec",
            "identifier": "801-123456",
            "entity_name": "Stonewater Advisers LLC",
            "status": "REGISTERED",
            "jurisdiction": "US",
            "last_updated": "2026-02-14T00:00:00Z",
            "permissions": ["Form ADV on file", "PFRD filer"],
            "metadata": {"pfrd": {"last_form_pf": "2025-12-31"}},
        }
    ],
    "finra": [
        {
            "registry": "finra",
            "identifier": "12345",
            "entity_name": "Jane Smith",
            "status": "ACTIVE",
            "jurisdiction": "US",
            "last_updated": "2026-02-19T00:00:00Z",
            "permissions": ["Series 7", "Series 24"],
            "metadata": {"firm": "Stonewater Securities LLC"},
        }
    ],
    "jfsa": [
        {
            "registry": "jfsa",
            "identifier": "CAESP-12345",
            "entity_name": "Snowdrop Exchange KK",
            "status": "REGISTERED",
            "jurisdiction": "JP",
            "last_updated": "2026-02-21T00:00:00Z",
            "permissions": ["Crypto-asset exchange service"],
            "metadata": {
                "cold_storage_ratio": 97,
                "hot_wallet_pct": 3,
                "audit_firm": "Stonewater Assurance",
            },
        }
    ],
    "nsdl": [
        {
            "registry": "nsdl",
            "identifier": "FPI12345",
            "entity_name": "Snowdrop Global Fund",
            "status": "ACTIVE",
            "jurisdiction": "IN",
            "last_updated": "2026-02-18T00:00:00Z",
            "permissions": ["Category I FPI"],
            "metadata": {
                "sector_exposure_pct": 21.5,
                "highest_company_pct": 8.4,
                "ddp": "Stonewater Bank India",
            },
        }
    ],
    "cdsl": [
        {
            "registry": "cdsl",
            "identifier": "FPICDSL6789",
            "entity_name": "Emerald Sovereign Fund",
            "status": "SUSPENDED",
            "jurisdiction": "IN",
            "last_updated": "2026-02-10T00:00:00Z",
            "permissions": ["Category II FPI"],
            "metadata": {
                "suspension_reason": "UBO documentation pending",
                "sector_exposure_pct": 34.0,
                "highest_company_pct": 12.0,
            },
        }
    ],
}


def get_registry_record(
    registry: str, identifier: str, *, force_refresh: bool = False
) -> RegistryRecord | None:
    """Return a single registry record by identifier."""

    normalized_registry = registry.lower().strip()
    normalized_identifier = identifier.strip()
    if not normalized_identifier:
        return None

    cache_key = (normalized_registry, normalized_identifier.lower())
    cached = _REGISTRY_CACHE.get(cache_key)
    now = time.time()
    if (
        cached
        and not force_refresh
        and (now - cached[0]) < _REGISTRY_TTL_SECONDS
    ):
        return cached[1]

    record = _load_registry_record(normalized_registry, normalized_identifier)
    if record:
        _REGISTRY_CACHE[cache_key] = (now, record)
    return record


def search_registry(
    registry: str,
    query: str,
    *,
    limit: int = 5,
    force_refresh: bool = False,
) -> list[RegistryRecord]:
    """Search the registry by entity name."""

    normalized_registry = registry.lower().strip()
    normalized_query = query.strip().lower()
    if not normalized_query:
        return []

    http_records = _http_search_registry(
        normalized_registry, normalized_query, limit, force_refresh
    )
    if http_records:
        return http_records[:limit]

    sample_records = _SAMPLE_REGISTRY_DATA.get(normalized_registry, [])
    matches = [
        record
        for record in sample_records
        if normalized_query in record.get("entity_name", "").lower()
    ]
    return matches[:limit]


def list_supported_registries() -> tuple[str, ...]:
    """Expose supported registry identifiers for status dashboards."""

    return tuple(sorted(_SAMPLE_REGISTRY_DATA))


def _load_registry_record(registry: str, identifier: str) -> RegistryRecord | None:
    record = _http_fetch_registry(registry, identifier)
    if record:
        return record

    sample_pool = _SAMPLE_REGISTRY_DATA.get(registry, [])
    for candidate in sample_pool:
        if candidate.get("identifier", "").lower() == identifier.lower():
            return candidate

    log_lesson(
        "compliance_registries",
        f"No registry match for {registry} identifier '{identifier}'",
    )
    return None


def _http_fetch_registry(registry: str, identifier: str) -> RegistryRecord | None:
    config = _REGISTRY_HTTP_CONFIG.get(registry)
    if not config:
        return None

    base_url = os.getenv(config.get("record_url_env", ""), "").strip()
    if not base_url:
        return None

    headers = _build_headers(config)
    url = f"{base_url.rstrip('/')}/{identifier}"
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        payload = response.json()
    except Exception as exc:  # pragma: no cover - network best effort
        log_lesson(
            "compliance_registries",
            f"{registry} registry HTTP fetch failed for '{identifier}': {exc}",
        )
        return None

    return _normalise_payload(registry, identifier, payload)


def _http_search_registry(
    registry: str, query: str, limit: int, force_refresh: bool
) -> list[RegistryRecord]:
    config = _REGISTRY_HTTP_CONFIG.get(registry)
    if not config:
        return []

    search_url = os.getenv(config.get("search_url_env", ""), "").strip()
    if not search_url:
        return []

    headers = _build_headers(config)
    params = {
        config.get("query_param", "q"): query,
        "limit": limit,
    }
    if force_refresh:
        params["fresh"] = "1"

    try:
        response = requests.get(
            search_url, headers=headers, params=params, timeout=10
        )
        response.raise_for_status()
        payload = response.json()
    except Exception as exc:  # pragma: no cover - network best effort
        log_lesson(
            "compliance_registries",
            f"{registry} registry search failed for '{query}': {exc}",
        )
        return []

    if isinstance(payload, dict):
        items = payload.get("results") or payload.get("items") or []
    else:
        items = payload

    records: list[RegistryRecord] = []
    for item in items:
        record = _normalise_payload(
            registry, str(item.get("id") or item.get("identifier") or query), item
        )
        if record:
            records.append(record)
    return records


def _build_headers(config: dict[str, Any]) -> dict[str, str]:
    headers: dict[str, str] = {"Accept": "application/json"}
    token_env = config.get("token_env")
    if token_env:
        token_value = os.getenv(token_env, "").strip()
        if token_value:
            headers["Authorization"] = f"Bearer {token_value}"
    session_env = config.get("session_env")
    if session_env:
        session_value = os.getenv(session_env, "").strip()
        if session_value:
            headers["X-Session-Token"] = session_value
    return headers


def _normalise_payload(
    registry: str, identifier: str, payload: dict[str, Any]
) -> RegistryRecord | None:
    if not isinstance(payload, dict):
        return None

    entity_name = (
        payload.get("entity_name")
        or payload.get("entityName")
        or payload.get("name")
        or ""
    )
    status = (
        payload.get("status")
        or payload.get("authorisation_status")
        or payload.get("state")
        or "UNKNOWN"
    )
    jurisdiction = payload.get("jurisdiction") or payload.get("country") or ""
    permissions: list[str] = []
    if isinstance(payload.get("permissions"), list):
        permissions = [str(p) for p in payload["permissions"]]
    elif isinstance(payload.get("authorisations"), list):
        permissions = [str(p) for p in payload["authorisations"]]

    last_updated = (
        payload.get("last_updated")
        or payload.get("lastUpdated")
        or payload.get("updated_at")
        or get_iso_timestamp()
    )

    return RegistryRecord(
        registry=registry,
        identifier=str(payload.get("identifier") or identifier),
        entity_name=str(entity_name),
        status=str(status).upper(),
        jurisdiction=str(jurisdiction or payload.get("domicile") or ""),
        last_updated=str(last_updated),
        permissions=permissions,
        metadata=payload,
    )
