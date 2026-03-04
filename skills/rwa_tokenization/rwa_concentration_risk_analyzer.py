"""Assess concentration risk across RWA collateral pools.
Computes exposure shares and HHI indicators to guide diversification."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Sequence
import logging

from skills.utils import log_lesson

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "rwa_concentration_risk_analyzer",
    "description": "Calculates concentration metrics for tokenized asset pools by asset type or geography.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "exposures": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "bucket": {"type": "string"},
                        "balance": {"type": "number"},
                    },
                    "required": ["bucket", "balance"],
                },
                "description": "Exposure by bucket",
            }
        },
        "required": ["exposures"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
            "data": {"type": "object"},
            "error": {"type": "string"},
        },
    },
}


def rwa_concentration_risk_analyzer(
    exposures: Sequence[dict[str, Any]],
    **_: Any,
) -> dict[str, Any]:
    """Measure concentration of exposures.

    Args:
        exposures: Balance per bucket.

    Returns:
        Dict with bucket shares and HHI.
    """
    try:
        total = sum(max(float(exp.get("balance", 0)), 0.0) for exp in exposures)
        if total <= 0:
            raise ValueError("exposures must sum to positive amount")
        bucket_data = []
        hhi = 0.0
        for exp in exposures:
            balance = max(float(exp.get("balance", 0)), 0.0)
            share_pct = balance / total * 100
            bucket_data.append({"bucket": exp.get("bucket", "bucket"), "share_pct": round(share_pct, 2)})
            hhi += (share_pct / 100) ** 2
        data = {
            "buckets": bucket_data,
            "hhi": round(hhi, 4),
            "diversification_flag": hhi < 0.2,
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("rwa_concentration_risk_analyzer failure: %s", exc)
        log_lesson(f"rwa_concentration_risk_analyzer: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
