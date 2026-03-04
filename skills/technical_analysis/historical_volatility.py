"""
Execuve Summary: Calculates realized historical volatility using multiple estimators (close-to-close, Parkinson, Garman-Klass, Yang-Zhang).
Inputs: prices (list[float]), highs (list[float]), lows (list[float]), opens (list[float]), closes (list[float]), period (int), method (str)
Outputs: hv_annualized (float), hv_daily (float), method_used (str), vol_cone_percentile (float), vol_regime (str)
MCP Tool Name: historical_volatility
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "historical_volatility",
    "description": "Computes realized volatility via close-to-close, Parkinson, Garman-Klass, or Yang-Zhang estimators.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "prices": {"type": "array", "description": "Generic closing price list for close_to_close."},
            "highs": {"type": "array", "description": "High prices for high-low based estimators."},
            "lows": {"type": "array", "description": "Low prices aligned with highs."},
            "opens": {"type": "array", "description": "Open prices for Garman-Klass/Yang-Zhang."},
            "closes": {"type": "array", "description": "Close prices for open-close estimators."},
            "period": {"type": "integer", "description": "Number of observations used in the volatility window."},
            "method": {"type": "string", "description": "Estimator: close_to_close, parkinson, garman_klass, yang_zhang."}
        },
        "required": ["period", "method"]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
            "data": {"type": "object"}
        },
        "required": ["status", "timestamp"]
    }
}

TRADING_DAYS = 252


def historical_volatility(**kwargs: Any) -> dict:
    """Supports multiple realized volatility estimators and compares current HV versus historical readings."""
    try:
        method = kwargs.get("method")
        period = kwargs.get("period")
        if not isinstance(method, str):
            raise ValueError("method must be a string")
        method = method.lower()
        if method not in {"close_to_close", "parkinson", "garman_klass", "yang_zhang"}:
            raise ValueError("method must be one of close_to_close, parkinson, garman_klass, yang_zhang")
        if not isinstance(period, int) or period < 2:
            raise ValueError("period must be >= 2")

        prices = kwargs.get("prices")
        highs = kwargs.get("highs")
        lows = kwargs.get("lows")
        opens = kwargs.get("opens")
        closes = kwargs.get("closes")

        def _validate_series(series: list[Any] | None, name: str) -> list[float]:
            if series is None:
                raise ValueError(f"{name} data required for {method}")
            if not isinstance(series, list) or len(series) < period:
                raise ValueError(f"{name} must be a list with at least 'period' points")
            clean = []
            for value in series:
                if not isinstance(value, (int, float)):
                    raise TypeError(f"{name} must be numeric")
                clean.append(float(value))
            return clean

        if method == "close_to_close":
            closes_clean = _validate_series(prices or closes, "prices")
            hv_daily = _close_to_close(closes_clean, period)
            hv_series = _rolling_hv(closes_clean, period, _close_to_close)
        elif method == "parkinson":
            highs_clean = _validate_series(highs, "highs")
            lows_clean = _validate_series(lows, "lows")
            _ensure_equal_length([highs_clean, lows_clean])
            hv_daily = _parkinson(highs_clean, lows_clean, period)
            hv_series = _rolling_hv((highs_clean, lows_clean), period, _parkinson)
        elif method == "garman_klass":
            opens_clean = _validate_series(opens, "opens")
            highs_clean = _validate_series(highs, "highs")
            lows_clean = _validate_series(lows, "lows")
            closes_clean = _validate_series(closes, "closes")
            _ensure_equal_length([opens_clean, highs_clean, lows_clean, closes_clean])
            hv_daily = _garman_klass(opens_clean, highs_clean, lows_clean, closes_clean, period)
            hv_series = _rolling_hv((opens_clean, highs_clean, lows_clean, closes_clean), period, _garman_klass)
        else:
            opens_clean = _validate_series(opens, "opens")
            highs_clean = _validate_series(highs, "highs")
            lows_clean = _validate_series(lows, "lows")
            closes_clean = _validate_series(closes, "closes")
            _ensure_equal_length([opens_clean, highs_clean, lows_clean, closes_clean])
            hv_daily = _yang_zhang(opens_clean, highs_clean, lows_clean, closes_clean, period)
            hv_series = _rolling_hv((opens_clean, highs_clean, lows_clean, closes_clean), period, _yang_zhang)

        hv_annualized = hv_daily * math.sqrt(TRADING_DAYS)
        percentile = _percentile_rank(hv_daily, hv_series)
        if hv_annualized < 10:
            regime = "low"
        elif hv_annualized < 25:
            regime = "normal"
        elif hv_annualized < 40:
            regime = "high"
        else:
            regime = "extreme"

        return {
            "status": "success",
            "data": {
                "hv_annualized": hv_annualized,
                "hv_daily": hv_daily,
                "method_used": method,
                "vol_cone_percentile": percentile,
                "vol_regime": regime
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"historical_volatility failed: {e}")
        _log_lesson(f"historical_volatility: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


def _close_to_close(closes: list[float], period: int) -> float:
    log_returns = _log_returns(closes[-(period + 1):])
    if len(log_returns) < 1:
        raise ValueError("insufficient closes for volatility")
    mean_return = sum(log_returns) / len(log_returns)
    variance = sum((r - mean_return) ** 2 for r in log_returns) / (len(log_returns) - 1)
    return math.sqrt(variance)


def _parkinson(highs: list[float], lows: list[float], period: int) -> float:
    highs_window = highs[-period:]
    lows_window = lows[-period:]
    constant = 1 / (4 * math.log(2))
    variance = sum((math.log(h / l)) ** 2 for h, l in zip(highs_window, lows_window)) / period
    return math.sqrt(constant * variance)


def _garman_klass(opens: list[float], highs: list[float], lows: list[float], closes: list[float], period: int) -> float:
    window_slice = slice(-period, None)
    opens_w = opens[window_slice]
    highs_w = highs[window_slice]
    lows_w = lows[window_slice]
    closes_w = closes[window_slice]
    sum_term = 0.0
    for o, h, l, c in zip(opens_w, highs_w, lows_w, closes_w):
        log_hl = math.log(h / l)
        log_co = math.log(c / o)
        sum_term += 0.5 * (log_hl ** 2) - (2 * math.log(2) - 1) * (log_co ** 2)
    return math.sqrt(sum_term / period)


def _yang_zhang(opens: list[float], highs: list[float], lows: list[float], closes: list[float], period: int) -> float:
    slice_obj = slice(- (period + 1), None)
    opens_w = opens[slice_obj]
    highs_w = highs[slice_obj]
    lows_w = lows[slice_obj]
    closes_w = closes[slice_obj]
    if len(opens_w) < period + 1:
        raise ValueError("not enough data for Yang-Zhang")
    log_ro = []
    log_rc = []
    log_hl = []
    for idx in range(1, len(opens_w)):
        o = opens_w[idx]
        c_prev = closes_w[idx - 1]
        c = closes_w[idx]
        h = highs_w[idx]
        l = lows_w[idx]
        log_ro.append(math.log(o / c_prev))
        log_rc.append(math.log(c / o))
        log_hl.append(math.log(h / l))
    n = period
    k = 0.34 / (1 + (n + 1) / (n - 1))
    sigma_oo = sum(value ** 2 for value in log_ro[-n:]) / (n - 1)
    sigma_cc = sum(value ** 2 for value in log_rc[-n:]) / (n - 1)
    sigma_hl = sum(value ** 2 for value in log_hl[-n:]) / (n - 1) * 0.5
    variance = sigma_oo + k * sigma_cc + (1 - k) * sigma_hl
    return math.sqrt(variance)


def _log_returns(values: list[float]) -> list[float]:
    returns = []
    for idx in range(1, len(values)):
        if values[idx - 1] <= 0 or values[idx] <= 0:
            raise ValueError("prices must be positive for log returns")
        returns.append(math.log(values[idx] / values[idx - 1]))
    return returns


def _rolling_hv(data: Any, period: int, estimator: Any) -> list[float]:
    hv_values = []
    length = len(data[0]) if isinstance(data, tuple) else len(data)
    if length <= period:
        return []
    for end in range(period, length + 1):
        if isinstance(data, tuple):
            window_data = tuple(series[:end] for series in data)
        else:
            window_data = data[:end]
        try:
            if estimator == _close_to_close:
                hv = estimator(window_data, period)
            elif estimator == _parkinson:
                hv = estimator(window_data[0], window_data[1], period)
            elif estimator == _garman_klass:
                hv = estimator(window_data[0], window_data[1], window_data[2], window_data[3], period)
            else:
                hv = estimator(window_data[0], window_data[1], window_data[2], window_data[3], period)
            hv_values.append(hv)
        except ValueError:
            continue
    return hv_values


def _percentile_rank(value: float, samples: list[float]) -> float:
    if not samples:
        return 1.0
    sorted_samples = sorted(samples)
    count = sum(1 for sample in sorted_samples if sample <= value)
    return count / len(sorted_samples)


def _ensure_equal_length(series_list: list[list[float]]) -> None:
    lengths = {len(series) for series in series_list}
    if len(lengths) != 1:
        raise ValueError("input series must have equal lengths")


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
