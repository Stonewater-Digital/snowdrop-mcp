"""
Executive Summary: Audits fiat-to-crypto on-ramp activity for volume trends, fee analysis, and anomalous daily spikes over a specified period.
Inputs: onramp_data (list[dict]: date, fiat_amount, crypto_received, exchange, fee_pct), period_days (int)
Outputs: total_volume (float), avg_fee_pct (float), daily_velocity (float), anomalies (list), trend (str)
MCP Tool Name: fiat_to_crypto_onramp_audit
"""
import os
import logging
from typing import Any
from datetime import datetime, timezone
from collections import defaultdict

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "fiat_to_crypto_onramp_audit",
    "description": "Audits fiat-to-crypto on-ramp transactions for volume, fees, velocity, and anomalous spikes.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "onramp_data": {
                "type": "array",
                "description": "List of on-ramp transaction records",
                "items": {
                    "type": "object",
                    "properties": {
                        "date": {"type": "string", "description": "ISO date string YYYY-MM-DD"},
                        "fiat_amount": {"type": "number", "description": "Fiat currency amount converted"},
                        "crypto_received": {"type": "number", "description": "Crypto units received"},
                        "exchange": {"type": "string", "description": "Exchange or provider name"},
                        "fee_pct": {"type": "number", "description": "Fee as percentage of transaction"}
                    },
                    "required": ["date", "fiat_amount", "fee_pct"]
                }
            },
            "period_days": {"type": "integer", "description": "Analysis window in days", "minimum": 1}
        },
        "required": ["onramp_data", "period_days"]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "total_volume": {"type": "number"},
                    "avg_fee_pct": {"type": "number"},
                    "daily_velocity": {"type": "number"},
                    "anomalies": {"type": "array"},
                    "trend": {"type": "string"}
                }
            },
            "timestamp": {"type": "string"}
        },
        "required": ["status", "data", "timestamp"]
    }
}

# Anomaly threshold: flag days exceeding this multiple of the average daily volume
SPIKE_MULTIPLIER = 2.0


def fiat_to_crypto_onramp_audit(
    onramp_data: list[dict[str, Any]],
    period_days: int,
    **kwargs: Any
) -> dict[str, Any]:
    """Audit fiat-to-crypto on-ramp activity for anomalies and trend.

    Aggregates transactions by date, computes total volume and fees,
    calculates daily velocity (total_volume / period_days), and flags
    any day whose volume exceeds SPIKE_MULTIPLIER times the average.
    Trend is determined by comparing first-half vs second-half average volume.

    Args:
        onramp_data: List of transaction dicts. Each must have:
            - date (str): ISO-8601 date 'YYYY-MM-DD'.
            - fiat_amount (float): Amount of fiat converted.
            - fee_pct (float): Fee charged as a percentage.
            Optional keys: 'crypto_received' (float), 'exchange' (str).
        period_days: The reporting period in days over which velocity is
            calculated. Must be >= 1.
        **kwargs: Ignored extra keyword arguments.

    Returns:
        dict: Standard Snowdrop response envelope with keys:
            - status (str): 'success' or 'error'.
            - data (dict): Audit results including total_volume, avg_fee_pct,
              daily_velocity, anomalies list, trend string, daily_breakdown,
              exchange_breakdown, and period_days.
            - timestamp (str): ISO-8601 UTC timestamp.
    """
    try:
        if not isinstance(onramp_data, list) or len(onramp_data) == 0:
            raise ValueError("onramp_data must be a non-empty list")

        period_days = int(period_days)
        if period_days < 1:
            raise ValueError("period_days must be >= 1")

        # Aggregate by date
        daily_volume: dict[str, float] = defaultdict(float)
        daily_fees: dict[str, list[float]] = defaultdict(list)
        exchange_volume: dict[str, float] = defaultdict(float)

        total_volume: float = 0.0
        total_fee_weighted: float = 0.0

        for record in onramp_data:
            date = str(record.get("date", "unknown"))
            fiat_amount = float(record.get("fiat_amount", 0.0))
            fee_pct = float(record.get("fee_pct", 0.0))
            exchange = str(record.get("exchange", "unknown"))

            daily_volume[date] += fiat_amount
            daily_fees[date].append(fee_pct)
            exchange_volume[exchange] += fiat_amount
            total_volume += fiat_amount
            total_fee_weighted += fee_pct * fiat_amount

        avg_fee_pct: float = (
            round(total_fee_weighted / total_volume, 6) if total_volume > 0 else 0.0
        )
        daily_velocity: float = round(total_volume / period_days, 4)

        # Build sorted daily breakdown
        sorted_dates = sorted(daily_volume.keys())
        daily_breakdown: list[dict[str, Any]] = [
            {
                "date": d,
                "volume": round(daily_volume[d], 2),
                "avg_fee_pct": round(sum(daily_fees[d]) / len(daily_fees[d]), 4),
                "tx_count": len(daily_fees[d]),
            }
            for d in sorted_dates
        ]

        # Compute average daily volume for anomaly detection
        avg_daily = total_volume / len(daily_volume) if daily_volume else 0.0
        spike_threshold = avg_daily * SPIKE_MULTIPLIER

        anomalies: list[dict[str, Any]] = []
        for d in sorted_dates:
            vol = daily_volume[d]
            if vol > spike_threshold:
                anomalies.append({
                    "date": d,
                    "volume": round(vol, 2),
                    "avg_daily_volume": round(avg_daily, 2),
                    "spike_ratio": round(vol / avg_daily, 4),
                    "threshold": round(spike_threshold, 2),
                    "severity": "HIGH" if vol > avg_daily * 4 else "MEDIUM",
                })

        # Trend analysis: compare first half vs second half of sorted dates
        trend: str = "INSUFFICIENT_DATA"
        if len(sorted_dates) >= 4:
            mid = len(sorted_dates) // 2
            first_half_avg = sum(daily_volume[d] for d in sorted_dates[:mid]) / mid
            second_half_avg = sum(daily_volume[d] for d in sorted_dates[mid:]) / (len(sorted_dates) - mid)

            pct_change = (second_half_avg - first_half_avg) / first_half_avg * 100 if first_half_avg > 0 else 0.0

            if pct_change > 20:
                trend = f"INCREASING ({pct_change:+.1f}% first-half vs second-half)"
            elif pct_change < -20:
                trend = f"DECREASING ({pct_change:+.1f}% first-half vs second-half)"
            else:
                trend = f"STABLE ({pct_change:+.1f}% first-half vs second-half)"

        # Exchange breakdown
        exchange_breakdown: list[dict[str, Any]] = sorted(
            [
                {
                    "exchange": ex,
                    "volume": round(vol, 2),
                    "pct_of_total": round(vol / total_volume * 100, 4) if total_volume > 0 else 0.0,
                }
                for ex, vol in exchange_volume.items()
            ],
            key=lambda x: x["volume"],
            reverse=True,
        )

        result: dict[str, Any] = {
            "total_volume": round(total_volume, 2),
            "avg_fee_pct": avg_fee_pct,
            "daily_velocity": daily_velocity,
            "anomalies": anomalies,
            "anomaly_count": len(anomalies),
            "trend": trend,
            "period_days": period_days,
            "active_days": len(daily_volume),
            "daily_breakdown": daily_breakdown,
            "exchange_breakdown": exchange_breakdown,
            "spike_threshold_usd": round(spike_threshold, 2),
        }

        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        logger.error(f"fiat_to_crypto_onramp_audit failed: {e}")
        _log_lesson(f"fiat_to_crypto_onramp_audit: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(message: str) -> None:
    """Append a lesson/error entry to the shared lessons log.

    Args:
        message: Human-readable error or lesson description to append.
    """
    try:
        os.makedirs("logs", exist_ok=True)
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except Exception as log_err:
        logger.warning(f"_log_lesson write failed: {log_err}")
