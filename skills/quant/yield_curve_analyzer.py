"""Analyze shape of yield curve and implied forwards."""
from __future__ import annotations

import math
from datetime import datetime, timezone
from typing import Any, Iterable

TOOL_META: dict[str, Any] = {
    "name": "yield_curve_analyzer",
    "description": "Builds spot discounts and forward rates to classify curve shape.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "par_yields": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "tenor_years": {"type": "number"},
                        "yield_pct": {"type": "number"},
                    },
                    "required": ["tenor_years", "yield_pct"],
                },
            },
        },
        "required": ["par_yields"],
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


def yield_curve_analyzer(par_yields: Iterable[dict[str, float]], **_: Any) -> dict[str, Any]:
    """Return discount factors, forwards, and shape classification."""
    try:
        nodes = sorted((node for node in par_yields), key=lambda item: item["tenor_years"])
        if not nodes:
            raise ValueError("par_yields must include at least one tenor")
        curve = []
        forwards = []
        for node in nodes:
            tenor = float(node["tenor_years"])
            rate = float(node["yield_pct"]) / 100
            discount = (1 + rate) ** (-tenor)
            curve.append(
                {
                    "tenor_years": tenor,
                    "yield_pct": round(rate * 100, 3),
                    "discount_factor": round(discount, 6),
                }
            )
        for first, second in zip(curve, curve[1:]):
            delta_t = second["tenor_years"] - first["tenor_years"]
            if delta_t <= 0:
                continue
            d1 = first["discount_factor"]
            d2 = second["discount_factor"]
            if not d2:
                continue
            fwd = (d1 / d2) ** (1 / delta_t) - 1
            forwards.append(
                {
                    "start": first["tenor_years"],
                    "end": second["tenor_years"],
                    "forward_rate_pct": round(fwd * 100, 3),
                }
            )
        slope = curve[-1]["yield_pct"] - curve[0]["yield_pct"]
        curvature = curve[len(curve) // 2]["yield_pct"] - (curve[0]["yield_pct"] + curve[-1]["yield_pct"]) / 2
        shape = "steep" if slope > 0.5 else "flat" if abs(slope) <= 0.1 else "inverted" if slope < -0.1 else "humped"
        data = {
            "curve_nodes": curve,
            "forward_rates": forwards,
            "slope_bps": round(slope * 100, 2),
            "curvature_bps": round(curvature * 100, 2),
            "shape_classification": shape,
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        _log_lesson(f"yield_curve_analyzer: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(message: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
