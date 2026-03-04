"""Estimate basis risk from hedge parameters."""
from __future__ import annotations

import math
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "basis_risk_calculator",
    "description": (
        "Quantifies commodity hedge basis risk. Computes hedged portfolio volatility, "
        "hedge effectiveness (R²), optimal hedge ratio (minimum-variance), and basis differential."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "spot_price": {
                "type": "number",
                "description": "Current spot price of the asset being hedged (must be > 0).",
            },
            "futures_price": {
                "type": "number",
                "description": "Current futures price used as the hedge instrument (must be > 0).",
            },
            "asset_vol_pct": {
                "type": "number",
                "description": "Annualized volatility of the spot asset in % (must be > 0).",
            },
            "futures_vol_pct": {
                "type": "number",
                "description": (
                    "Annualized volatility of the futures contract in % (must be > 0). "
                    "If omitted, assumed equal to asset_vol_pct."
                ),
            },
            "hedge_ratio": {
                "type": "number",
                "default": 1.0,
                "description": "Hedge ratio h (futures position / spot position). Typically 0–1.",
            },
            "correlation": {
                "type": "number",
                "default": 0.9,
                "description": "Correlation between spot and futures returns (−1 to 1).",
            },
        },
        "required": ["spot_price", "futures_price", "asset_vol_pct"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["success", "error"]},
            "basis_value": {"type": "number"},
            "basis_pct_of_spot": {"type": "number"},
            "hedged_volatility_pct": {"type": "number"},
            "unhedged_volatility_pct": {"type": "number"},
            "hedge_effectiveness_pct": {"type": "number"},
            "optimal_hedge_ratio": {"type": "number"},
            "timestamp": {"type": "string"},
        },
    },
}


def basis_risk_calculator(
    spot_price: float,
    futures_price: float,
    asset_vol_pct: float,
    futures_vol_pct: float | None = None,
    hedge_ratio: float = 1.0,
    correlation: float = 0.9,
    **_: Any,
) -> dict[str, Any]:
    """Return basis differential and hedge effectiveness metrics.

    Args:
        spot_price: Current spot price of the asset (must be > 0).
        futures_price: Current futures price (must be > 0).
        asset_vol_pct: Annualized spot volatility in % (must be > 0).
        futures_vol_pct: Annualized futures volatility in %. Defaults to asset_vol_pct.
        hedge_ratio: Fraction of spot exposure hedged with futures (h). Default 1.0.
        correlation: Pearson correlation between spot and futures returns. Default 0.9.

    Returns:
        dict with status, basis_value, basis_pct_of_spot, hedged_volatility_pct,
        hedge_effectiveness_pct (R²), and optimal_hedge_ratio.

    Hedged portfolio variance (Ederington 1979):
        Var_hedged = σ_S² + h² * σ_F² - 2 * h * ρ * σ_S * σ_F

    Hedge effectiveness = R² = 1 - Var_hedged / Var_unhedged
        At optimal h* = ρ * σ_S / σ_F, this simplifies to R² = ρ².

    Optimal hedge ratio (minimum-variance):
        h* = ρ * σ_S / σ_F
    """
    try:
        if spot_price <= 0:
            raise ValueError("spot_price must be positive")
        if futures_price <= 0:
            raise ValueError("futures_price must be positive")
        if asset_vol_pct <= 0:
            raise ValueError("asset_vol_pct must be positive")
        if not -1.0 <= correlation <= 1.0:
            raise ValueError("correlation must be in [-1, 1]")

        sigma_s = asset_vol_pct  # spot vol in %
        sigma_f = futures_vol_pct if futures_vol_pct is not None else asset_vol_pct
        if sigma_f <= 0:
            raise ValueError("futures_vol_pct must be positive")
        rho = correlation
        h = hedge_ratio

        basis_value = spot_price - futures_price
        basis_pct = (basis_value / spot_price) * 100.0

        # Hedged variance using Ederington formula (in vol-% units)
        var_unhedged = sigma_s ** 2
        var_hedged = sigma_s ** 2 + h ** 2 * sigma_f ** 2 - 2.0 * h * rho * sigma_s * sigma_f
        var_hedged = max(var_hedged, 0.0)
        hedged_vol = math.sqrt(var_hedged)

        # Hedge effectiveness: R² = 1 - Var_hedged / Var_unhedged
        effectiveness = 1.0 - var_hedged / var_unhedged if var_unhedged > 0 else 0.0

        # Optimal (minimum-variance) hedge ratio: h* = ρ * σ_S / σ_F
        optimal_h = rho * sigma_s / sigma_f if sigma_f > 0 else 0.0

        return {
            "status": "success",
            "basis_value": round(basis_value, 4),
            "basis_pct_of_spot": round(basis_pct, 4),
            "hedged_volatility_pct": round(hedged_vol, 4),
            "unhedged_volatility_pct": round(sigma_s, 4),
            "hedge_effectiveness_pct": round(effectiveness * 100.0, 2),
            "optimal_hedge_ratio": round(optimal_h, 4),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("basis_risk_calculator", str(exc))
        return {
            "status": "error",
            "error": str(exc),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
