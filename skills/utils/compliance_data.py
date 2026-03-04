"""Shared compliance data utilities for sanctions/AML feeds.

Centralises live and fallback sanctions data retrieval so individual skills no
longer fetch OFAC/FATF/partner feeds independently. The helpers below expose a
cached aggregate sanctions feed plus a convenience accessor that returns the
sanctioned address set for a specific chain.
"""
from __future__ import annotations

import os
import time
from typing import Any, Callable, TypedDict, Sequence

import requests

from .logging import log_lesson
from .time import get_iso_timestamp


class SanctionsRecord(TypedDict):
    """Typed representation of a sanctioned wallet entry."""

    address: str
    chain: str
    program: str
    source: str
    labels: list[str]
    last_updated: str


_SANCTIONS_TTL_SECONDS = 3600
_DEFAULT_SOURCES = ("ofac", "fatf", "sample")

_SANCTIONS_CACHE: dict[str, tuple[float, list[SanctionsRecord]]] = {}

_SAMPLE_SANCTIONS: dict[str, list[dict[str, Any]]] = {
    "ethereum": [
        {
            "address": "0x8576acc5c05d6ce88f4e49bf65bdf0c62f91353c",
            "program": "OFAC-SDN",
            "labels": ["Lazarus Group proxy"],
        },
        {
            "address": "0xd882cfc20f52f2599d84b8e8d58c7fb62cfe344b",
            "program": "OFAC-SDN",
            "labels": ["Tornado Cash"],
        },
        {
            "address": "0x722122df12d4e14e13ac3b6895a86e84145b6967",
            "program": "OFAC-SDN",
            "labels": ["Tornado Cash Router"],
        },
        {
            "address": "0xdd4c48c0b24039969fc16d1cdf626eab821d3384",
            "program": "OFAC-SDN",
            "labels": ["Tornado Cash 0.1 ETH pool"],
        },
        {
            "address": "0xd90e2f925da726b50c4ed8d0fb90ad053324f31b",
            "program": "OFAC-SDN",
            "labels": ["Tornado Cash 1 ETH pool"],
        },
        {
            "address": "0x910cbd523d972eb0a6f4cae4618ad62622b39dbf",
            "program": "OFAC-SDN",
            "labels": ["Tornado Cash 10 ETH pool"],
        },
        {
            "address": "0xa160cdab225685da1d56aa342ad8841c3b53f291",
            "program": "OFAC-SDN",
            "labels": ["Tornado Cash 100 ETH pool"],
        },
        {
            "address": "0xfd8610d20aa15b7b2e3be39b396a1bc3516c7144",
            "program": "OFAC-SDN",
            "labels": ["OFAC mixer"],
        },
        {
            "address": "0x3cbded43efdaf0fc77b9c55f6fc9988fcc9b037d",
            "program": "OFAC-SDN",
            "labels": ["High-risk exchange deposit"],
        },
        {
            "address": "0xfe9d99ef9b90d0a1e4b8cc5c62a06eb6d46aa9b",
            "program": "OFAC-SDN",
            "labels": ["High-risk cluster"],
        },
        {
            "address": "0x2f50508a8a3d323b91336fa3ea6ae50e55f32185",
            "program": "OFAC-SDN",
            "labels": ["Lazarus Group"],
        },
    ],
    "solana": [
        {
            "address": "7Np41oeYqpe1Rvu6vNcgZZCkp9EFxS63sBkFHMrDMVP",
            "program": "OFAC-SDN",
            "labels": ["Lazarus cluster"],
        },
        {
            "address": "CgX8eXRkCRQ8FTBL3P3jYtqVJvVHB7X2Gd6Qs8VsEhY",
            "program": "OFAC-SDN",
            "labels": ["Sanctioned mixer"],
        },
    ],
    "ton": [
        {
            "address": "EQBc_FOLoyMa7CHxbJKRj_i1qC6FO-YIOBK8e8s-V3Rr",
            "program": "OFAC-SDN",
            "labels": ["DPRK-linked"],
        },
        {
            "address": "UQDa_wWlMN7FeI2NNx8REnT9fRRnqWfUb4b8q-q8Ys78",
            "program": "OFAC-SDN",
            "labels": ["Sanctioned entity"],
        },
    ],
}


def get_sanctions_feed(
    chains: Sequence[str] | None = None,
    sources: Sequence[str] | None = None,
    force_refresh: bool = False,
) -> dict[str, list[SanctionsRecord]]:
    """Return a sanctions feed keyed by chain.

    Args:
        chains: Optional chains to filter (e.g., ["ethereum"]). If omitted
            all chains contained in the selected sources are returned.
        sources: Optional sanctions sources. Defaults to OFAC + FATF + sample
            data. Available sources: ofac, fatf, sample, chainalysis, trm.
        force_refresh: When True, bypasses the cache for the requested sources.

    Returns:
        Dict keyed by chain ("ethereum", "solana", "ton") containing
        SanctionsRecord lists.
    """

    target_chains = {chain.lower() for chain in chains} if chains else None
    requested_sources = tuple(sources) if sources else _select_default_sources()
    feed: dict[str, list[SanctionsRecord]] = {}

    for source in requested_sources:
        loader = _SANCTION_LOADERS.get(source)
        if not loader:
            raise ValueError(
                f"Unsupported sanctions source '{source}'. Valid options: "
                f"{', '.join(sorted(_SANCTION_LOADERS))}"
            )
        records = _pull_with_cache(source, loader, force_refresh)
        for record in records:
            if target_chains and record["chain"] not in target_chains:
                continue
            feed.setdefault(record["chain"], []).append(record)

    return feed


def get_sanctioned_addresses(
    chain: str,
    sources: Sequence[str] | None = None,
    force_refresh: bool = False,
) -> set[str]:
    """Return a deduplicated set of sanctioned addresses for a chain."""

    normalized_chain = chain.lower().strip()
    feed = get_sanctions_feed(
        chains=[normalized_chain], sources=sources, force_refresh=force_refresh
    )
    records = feed.get(normalized_chain, [])
    addresses: set[str] = set()
    for record in records:
        addresses.add(_normalise_address(record["address"], normalized_chain))
    return addresses


def list_available_sanctions_sources() -> tuple[str, ...]:
    """Expose supported sanctions sources for status pages/tests."""

    return tuple(sorted(_SANCTION_LOADERS))


def _select_default_sources() -> tuple[str, ...]:
    """Include partner feeds only when credentials are present."""

    defaults = list(_DEFAULT_SOURCES)
    if os.getenv("CHAINALYSIS_API_KEY"):
        defaults.append("chainalysis")
    if os.getenv("TRM_API_KEY"):
        defaults.append("trm")
    return tuple(defaults)


def _pull_with_cache(
    source: str, loader: Callable[[], list[SanctionsRecord]], force_refresh: bool
) -> list[SanctionsRecord]:
    entry = _SANCTIONS_CACHE.get(source)
    now = time.time()
    if (
        entry
        and not force_refresh
        and now - entry[0] < _SANCTIONS_TTL_SECONDS
    ):
        return entry[1]

    records = loader()
    _SANCTIONS_CACHE[source] = (now, records)
    return records


def _load_ofac_feed() -> list[SanctionsRecord]:
    url = os.getenv("OFAC_SANCTIONS_URL")
    if not url:
        return _build_sample_records("ofac")

    try:
        entries = _download_remote_feed(url)
        return _normalise_entries(entries, default_chain="ethereum", default_source="ofac")
    except Exception as exc:  # noqa: BLE001
        log_lesson(f"compliance_data: Failed to download OFAC feed via {url}: {exc}")
        return _build_sample_records("ofac")


def _load_fatf_feed() -> list[SanctionsRecord]:
    url = os.getenv("FATF_SANCTIONS_URL")
    if not url:
        return _build_sample_records("fatf")
    try:
        entries = _download_remote_feed(url)
        return _normalise_entries(entries, default_chain="ethereum", default_source="fatf")
    except Exception as exc:  # noqa: BLE001
        log_lesson(f"compliance_data: Failed to download FATF feed via {url}: {exc}")
        return _build_sample_records("fatf")


def _load_chainalysis_feed() -> list[SanctionsRecord]:
    api_key = os.getenv("CHAINALYSIS_API_KEY")
    if not api_key:
        raise ValueError(
            "CHAINALYSIS_API_KEY is required for the Chainalysis sanctions feed. "
            "Populate it in .env (see .env.template)."
        )

    url = os.getenv(
        "CHAINALYSIS_SANCTIONS_URL",
        "https://public.chainalysis.com/api/v1/sanctions",
    )
    headers = {"X-API-Key": api_key}
    try:
        entries = _download_remote_feed(url, headers=headers)
        return _normalise_entries(entries, default_chain="ethereum", default_source="chainalysis")
    except Exception as exc:  # noqa: BLE001
        log_lesson(f"compliance_data: Chainalysis feed error via {url}: {exc}")
        return []


def _load_trm_feed() -> list[SanctionsRecord]:
    api_key = os.getenv("TRM_API_KEY")
    if not api_key:
        raise ValueError(
            "TRM_API_KEY is required for the TRM sanctions feed. "
            "Populate it in .env (see .env.template)."
        )

    url = os.getenv("TRM_SANCTIONS_URL", "https://api.trmlabs.com/public/v1/sanctions")
    headers = {"Authorization": f"Bearer {api_key}"}
    try:
        entries = _download_remote_feed(url, headers=headers)
        return _normalise_entries(entries, default_chain="ethereum", default_source="trm")
    except Exception as exc:  # noqa: BLE001
        log_lesson(f"compliance_data: TRM feed error via {url}: {exc}")
        return []


def _load_sample_feed() -> list[SanctionsRecord]:
    return _build_sample_records("sample")


def _download_remote_feed(url: str, headers: dict[str, str] | None = None) -> list[Any]:
    response = requests.get(url, headers=headers, timeout=20)
    response.raise_for_status()
    payload = response.json()
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for key in ("data", "results", "records", "sanctions"):
            value = payload.get(key)
            if isinstance(value, list):
                return value
    raise ValueError("Remote sanctions feed response is not a JSON list")


def _normalise_entries(
    entries: list[Any],
    default_chain: str,
    default_source: str,
) -> list[SanctionsRecord]:
    feed: list[SanctionsRecord] = []
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        address = str(
            entry.get("address")
            or entry.get("wallet")
            or entry.get("walletAddress")
            or entry.get("value")
            or ""
        ).strip()
        if not address:
            continue
        chain = str(entry.get("chain") or default_chain).lower().strip()
        record = SanctionsRecord(
            address=_normalise_address(address, chain),
            chain=chain,
            program=str(entry.get("program") or entry.get("list") or "UNKNOWN").upper(),
            source=default_source,
            labels=_normalise_labels(entry.get("labels")),
            last_updated=str(entry.get("last_updated") or entry.get("timestamp") or get_iso_timestamp()),
        )
        feed.append(record)
    return feed


def _build_sample_records(source: str) -> list[SanctionsRecord]:
    feed: list[SanctionsRecord] = []
    timestamp = get_iso_timestamp()
    for chain, entries in _SAMPLE_SANCTIONS.items():
        for entry in entries:
            feed.append(
                SanctionsRecord(
                    address=_normalise_address(entry["address"], chain),
                    chain=chain,
                    program=entry.get("program", "OFAC-SDN"),
                    source=source,
                    labels=list(entry.get("labels", [])),
                    last_updated=timestamp,
                )
            )
    return feed


def _normalise_labels(labels: Any) -> list[str]:
    if not labels:
        return []
    if isinstance(labels, list):
        return [str(label) for label in labels if label]
    return [str(labels)]


def _normalise_address(address: str, chain: str) -> str:
    if chain == "ethereum":
        return address.lower()
    return address


_SANCTION_LOADERS: dict[str, Callable[[], list[SanctionsRecord]]] = {
    "ofac": _load_ofac_feed,
    "fatf": _load_fatf_feed,
    "chainalysis": _load_chainalysis_feed,
    "trm": _load_trm_feed,
    "sample": _load_sample_feed,
}
