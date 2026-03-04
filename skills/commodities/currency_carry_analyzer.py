"""Evaluate currency carry trades using interest differentials."""
from __future__ import annotations

import math
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "currency_carry_analyzer",
    "description": (
        "Calculates carry yield (interest rate differential) for FX pairs, "
        "checks covered interest parity (CIP) deviation against observed forwards, "
        "and ranks pairs by carry attractiveness."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "pairs": {
                "type": "array",
                "description": "List of FX pair carry inputs.",
                "items": {
                    "type": "object",
                    "properties": {
                        "base_currency": {
                            "type": "string",
                            "description": "Base currency code (e.g. 'AUD').",
                        },
                        "quote_currency": {
                            "type": "string",
                            "description": "Quote currency code (e.g. 'JPY').",
                        },
                        "base_interest_rate_pct": {
                            "type": "number",
                            "description": "Annual interest rate for base currency as %.",
                        },
                        "quote_interest_rate_pct": {
                            "type": "number",
                            "description": "Annual interest rate for quote currency as %.",
                        },
                        "spot_rate": {
                            "type": "number",
                            "description": "Current spot FX rate (base/quote), must be > 0.",
                        },
                        "forward_rate": {
                            "type": ["number", "null"],
                            "default": None,
                            "description": "Observed 1-year forward rate (optional, for CIP check).",
                        },
                    },
                    "required": [
                        "base_currency",
                        "quote_currency",
                        "base_interest_rate_pct",
                        "quote_interest_rate_pct",
                        "spot_rate",
                    ],
                },
                "minItems": 1,
            },
            "cip_threshold_pct": {
                "type": "number",
                "default": 0.25,
                "description": "CIP deviation threshold in % to flag arbitrage (default 0.25%).",
            },
        },
        "required": ["pairs"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["success", "error"]},
            "pairs": {"type": "array"},
            "best_carry_pair": {"type": ["string", "null"]},
            "cip_violations": {"type": "array"},
            "risk_warning": {"type": "string"},
            "timestamp": {"type": "string"},
        },
    },
}


def currency_carry_analyzer(
    pairs: list[dict[str, Any]],
    cip_threshold_pct: float = 0.25,
    **_: Any,
) -> dict[str, Any]:
    """Return carry stats and CIP checks for FX pairs.

    Args:
        pairs: List of FX pair dicts with currency codes, interest rates, spot, and optional forward.
        cip_threshold_pct: Threshold in % for flagging CIP violations (default 0.25%).

    Returns:
        dict with status, per-pair carry metrics, best_carry_pair, cip_violations, risk_warning.

    Carry (uncovered interest parity logic):
        carry_pct = base_rate - quote_rate
        A positive carry means the investor earns the differential by being long base.

    CIP theoretical forward (1-year, continuous):
        F_cip = S * exp((r_quote - r_base) / 100)

    CIP deviation:
        |F_observed - F_cip| / F_cip * 100 > threshold => violation flagged.

    Note: carry_bps in output is (base_rate - quote_rate) * 100 (basis points).
    """
    try:
        if not pairs:
            raise ValueError("pairs list cannot be empty")

        results = []
        best_carry = -1e9
        best_pair_name: str | None = None
        cip_violations = []

        for pair in pairs:
            base_rate = float(pair.get("base_interest_rate_pct", 0))
            quote_rate = float(pair.get("quote_interest_rate_pct", 0))
            spot = float(pair["spot_rate"])
            forward = pair.get("forward_rate")
            base_ccy = str(pair.get("base_currency", ""))
            quote_ccy = str(pair.get("quote_currency", ""))

            if spot <= 0:
                raise ValueError(f"spot_rate must be positive for {base_ccy}/{quote_ccy}")

            carry_pct = base_rate - quote_rate
            pair_name = f"{base_ccy}/{quote_ccy}"

            if carry_pct > best_carry:
                best_carry = carry_pct
                best_pair_name = pair_name

            # CIP theoretical 1-year forward (continuous): F = S * exp((r_q - r_b) / 100)
            cip_fwd = spot * math.exp((quote_rate - base_rate) / 100.0)

            cip_dev_pct: float | None = None
            if forward is not None:
                fwd = float(forward)
                cip_dev_pct = abs(fwd - cip_fwd) / cip_fwd * 100.0 if cip_fwd > 0 else None
                if cip_dev_pct is not None and cip_dev_pct > cip_threshold_pct:
                    cip_violations.append(
                        {
                            "pair": pair_name,
                            "observed_forward": round(fwd, 6),
                            "cip_forward": round(cip_fwd, 6),
                            "deviation_pct": round(cip_dev_pct, 4),
                        }
                    )

            results.append(
                {
                    "pair": pair_name,
                    "carry_pct": round(carry_pct, 4),
                    "carry_bps": round(carry_pct * 100.0, 1),
                    "cip_forward": round(cip_fwd, 6),
                    "observed_forward": round(float(forward), 6) if forward is not None else None,
                    "cip_deviation_pct": round(cip_dev_pct, 4) if cip_dev_pct is not None else None,
                }
            )

        # Sort by carry descending
        results.sort(key=lambda item: item["carry_pct"], reverse=True)
        risk_warning = (
            f"{len(cip_violations)} CIP violation(s) detected — potential arbitrage or bid/ask issues"
            if cip_violations
            else "No CIP violations — standard carry risk applies"
        )

        return {
            "status": "success",
            "pairs": results,
            "best_carry_pair": best_pair_name,
            "cip_violations": cip_violations,
            "risk_warning": risk_warning,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("currency_carry_analyzer", str(exc))
        return {
            "status": "error",
            "error": str(exc),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
