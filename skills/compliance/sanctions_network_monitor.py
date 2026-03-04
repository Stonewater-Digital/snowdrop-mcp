"""
Executive Summary: Monitors exposures against Snowdrop's sanctions feed and surfaces flagged wallets with severity tiers.

Inputs: exposures (list[dict]), chains (list[str], optional), sources (list[str], optional), alert_threshold_usd (float, optional), notify_thunder (bool, optional)
Outputs: status (str), data (flags/summary), timestamp (str)
MCP Tool Name: sanctions_network_monitor
"""
from __future__ import annotations

from typing import Any

from skills.utils import (
    SkillTelemetryEmitter,
    get_iso_timestamp,
    logger,
    log_lesson as _shared_log_lesson,
    record_submission_event,
)
from skills.utils.compliance_data import get_sanctions_feed

TOOL_META: dict[str, Any] = {
    "name": "sanctions_network_monitor",
    "description": "Cross-check wallet exposures against sanctions feeds and return flagged entities.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "exposures": {
                "type": "array",
                "items": {"type": "object"},
                "description": "List of exposures containing address, chain, and amount_usd.",
            },
            "chains": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Optional list of chains to query in the sanctions feed.",
            },
            "sources": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Sanctions sources to query (e.g., ofac, fatf, sample).",
            },
            "alert_threshold_usd": {
                "type": "number",
                "default": 500_000,
                "description": "Trigger Thunder escalation when flagged exposure exceeds this USD amount.",
            },
            "notify_thunder": {
                "type": "boolean",
                "default": False,
                "description": "Send Thunder alert when threshold breached.",
            },
        },
        "required": ["exposures"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["ok", "error"]},
            "data": {
                "type": "object",
                "properties": {
                    "flags": {"type": "array", "items": {"type": "object"}},
                    "summary": {"type": "object"},
                },
            },
            "timestamp": {"type": "string", "format": "date-time"},
            "audit_log_reference": {
                "type": "string",
                "description": "Reference ID for compliance audit log entry",
            },
        },
        "required": ["status", "timestamp"],
    },
}


def sanctions_network_monitor(
    exposures: list[dict[str, Any]],
    chains: list[str] | None = None,
    sources: list[str] | None = None,
    alert_threshold_usd: float = 500_000,
    notify_thunder: bool = False,
) -> dict[str, Any]:
    """Check exposures against Snowdrop's sanctions feed."""
    emitter = SkillTelemetryEmitter(
        "sanctions_network_monitor",
        {"exposures": len(exposures or []), "alert_threshold_usd": alert_threshold_usd},
    )
    try:
        if not exposures:
            raise ValueError("exposures cannot be empty")

        target_chains = chains or sorted({str(item.get("chain", "")).lower() for item in exposures if item.get("chain")})
        feed = get_sanctions_feed(chains=target_chains, sources=sources)

        feed_lookup: dict[str, set[str]] = {
            chain: {record["address"].lower() for record in records}
            for chain, records in feed.items()
        }

        flags: list[dict[str, Any]] = []
        total_flagged_value = 0.0
        chain_breakdown: dict[str, float] = {}

        for exposure in exposures:
            chain = str(exposure.get("chain") or "").lower()
            address = str(exposure.get("address") or "").lower()
            amount = float(exposure.get("amount_usd") or 0.0)
            owner = exposure.get("owner") or "unknown"
            if not chain or not address:
                continue
            if address in feed_lookup.get(chain, set()):
                flags.append(
                    {
                        "address": address,
                        "chain": chain,
                        "amount_usd": round(amount, 2),
                        "owner": owner,
                    }
                )
                total_flagged_value += amount
                chain_breakdown[chain] = chain_breakdown.get(chain, 0.0) + amount

        summary = {
            "flagged_count": len(flags),
            "flagged_value_usd": round(total_flagged_value, 2),
            "chains": {chain: round(value, 2) for chain, value in chain_breakdown.items()},
        }
        emitter.record("ok", summary)

        if notify_thunder and total_flagged_value >= alert_threshold_usd and flags:
            _notify_thunder(
                f"Sanctions exposure {total_flagged_value:,.0f} USD across {len(flags)} wallets.",
                severity="CRITICAL" if total_flagged_value >= alert_threshold_usd * 2 else "WARNING",
            )

        data = {"flags": flags, "summary": summary}
        audit_entry = record_submission_event(
            "sanctions_network_monitor",
            "sanctions_monitor",
            status="success",
            payload=data,
            notes=[f"{flag['owner']}:{flag['address']}" for flag in flags] if flags else [],
            metadata={
                "alert_threshold_usd": alert_threshold_usd,
                "flagged_count": len(flags),
            },
        )
        return {
            "status": "ok",
            "data": data,
            "timestamp": get_iso_timestamp(),
            "audit_log_reference": audit_entry["reference_id"],
        }
    except Exception as exc:  # noqa: BLE001
        logger.error(f"sanctions_network_monitor failed: {exc}")
        _log_lesson("sanctions_network_monitor", str(exc))
        emitter.record("error", {"error": str(exc)})
        audit_entry = record_submission_event(
            "sanctions_network_monitor",
            "sanctions_monitor",
            status="error",
            payload={"error": str(exc)},
            notes=[str(exc)],
        )
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": get_iso_timestamp(),
            "audit_log_reference": audit_entry["reference_id"],
        }


def _notify_thunder(message: str, *, severity: str) -> None:
    """Send Thunder alert while tolerating missing env vars."""
    try:
        from skills.thunder_signal import thunder_signal

        thunder_signal(severity=severity, message=message)
    except Exception as exc:  # noqa: BLE001
        logger.warning(f"sanctions_network_monitor alert failed: {exc}")


def _log_lesson(skill_name: str, error: str) -> None:
    """Proxy shared lesson logger."""
    _shared_log_lesson(skill_name, error)
