"""Calculate Ichimoku Cloud components from price data.

MCP Tool Name: ichimoku_cloud_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "ichimoku_cloud_calculator",
    "description": "Calculate all five Ichimoku Cloud components: Tenkan-sen, Kijun-sen, Senkou Span A, Senkou Span B, and Chikou Span.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "highs": {
                "type": "array",
                "items": {"type": "number"},
                "description": "List of high prices (oldest to newest).",
            },
            "lows": {
                "type": "array",
                "items": {"type": "number"},
                "description": "List of low prices (oldest to newest).",
            },
            "closes": {
                "type": "array",
                "items": {"type": "number"},
                "description": "List of closing prices (oldest to newest).",
            },
        },
        "required": ["highs", "lows", "closes"],
    },
}


def _midpoint(data: list[float], period: int, idx: int) -> float | None:
    """Calculate (highest high + lowest low) / 2 over period ending at idx."""
    if idx < period - 1:
        return None
    window = data[idx - period + 1 : idx + 1]
    return (max(window) + min(window)) / 2


def ichimoku_cloud_calculator(
    highs: list[float],
    lows: list[float],
    closes: list[float],
) -> dict[str, Any]:
    """Calculate Ichimoku Cloud components."""
    try:
        n = len(highs)
        if n != len(lows) or n != len(closes):
            return {
                "status": "error",
                "data": {"error": "Highs, lows, and closes arrays must be the same length."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        if n < 52:
            return {
                "status": "error",
                "data": {"error": f"Need at least 52 data points for Ichimoku, got {n}."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        # Combine highs and lows for midpoint calculations
        all_data_h = highs
        all_data_l = lows

        # Tenkan-sen (Conversion Line): (9-period high + 9-period low) / 2
        tenkan: list[float | None] = []
        for i in range(n):
            if i < 8:
                tenkan.append(None)
            else:
                h = max(all_data_h[i - 8 : i + 1])
                l = min(all_data_l[i - 8 : i + 1])
                tenkan.append(round((h + l) / 2, 4))

        # Kijun-sen (Base Line): (26-period high + 26-period low) / 2
        kijun: list[float | None] = []
        for i in range(n):
            if i < 25:
                kijun.append(None)
            else:
                h = max(all_data_h[i - 25 : i + 1])
                l = min(all_data_l[i - 25 : i + 1])
                kijun.append(round((h + l) / 2, 4))

        # Senkou Span A: (Tenkan + Kijun) / 2, plotted 26 periods ahead
        senkou_a: list[float | None] = []
        for i in range(n):
            t = tenkan[i]
            k = kijun[i]
            if t is not None and k is not None:
                senkou_a.append(round((t + k) / 2, 4))
            else:
                senkou_a.append(None)

        # Senkou Span B: (52-period high + 52-period low) / 2, plotted 26 periods ahead
        senkou_b: list[float | None] = []
        for i in range(n):
            if i < 51:
                senkou_b.append(None)
            else:
                h = max(all_data_h[i - 51 : i + 1])
                l = min(all_data_l[i - 51 : i + 1])
                senkou_b.append(round((h + l) / 2, 4))

        # Chikou Span: current close plotted 26 periods back
        chikou = closes[:]

        latest_idx = n - 1
        latest_close = closes[latest_idx]
        latest_tenkan = tenkan[latest_idx]
        latest_kijun = kijun[latest_idx]
        latest_senkou_a = senkou_a[latest_idx]
        latest_senkou_b = senkou_b[latest_idx]

        # Signal interpretation
        signal = "neutral"
        if latest_tenkan is not None and latest_kijun is not None:
            if latest_tenkan > latest_kijun and latest_close > (latest_senkou_a or 0):
                signal = "bullish — price above cloud, Tenkan above Kijun"
            elif latest_tenkan < latest_kijun and latest_close < (latest_senkou_b or float("inf")):
                signal = "bearish — price below cloud, Tenkan below Kijun"
            elif latest_senkou_a is not None and latest_senkou_b is not None:
                cloud_top = max(latest_senkou_a, latest_senkou_b)
                cloud_bottom = min(latest_senkou_a, latest_senkou_b)
                if cloud_bottom <= latest_close <= cloud_top:
                    signal = "neutral — price inside the cloud (consolidation)"

        return {
            "status": "ok",
            "data": {
                "latest_tenkan_sen": latest_tenkan,
                "latest_kijun_sen": latest_kijun,
                "latest_senkou_span_a": latest_senkou_a,
                "latest_senkou_span_b": latest_senkou_b,
                "latest_close": latest_close,
                "signal": signal,
                "tenkan_sen": [v for v in tenkan[-26:] if v is not None],
                "kijun_sen": [v for v in kijun[-26:] if v is not None],
                "senkou_span_a": [v for v in senkou_a[-26:] if v is not None],
                "senkou_span_b": [v for v in senkou_b[-26:] if v is not None],
                "note": "Senkou Spans are normally plotted 26 periods ahead. Values shown are current-period calculations.",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
