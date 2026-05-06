---
skill: managed_futures_trend_signal
category: alternative_investments
description: Computes normalized trend-following signals using short/medium/long moving averages and breakout statistics inspired by CTA models. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: price_series, short_window, medium_window, long_window
---

# Managed Futures Trend Signal

## Description
Computes normalized trend-following signals using short, medium, and long moving average crossovers and breakout statistics, inspired by systematic CTA models. Outputs a composite signal score and individual timeframe signals. Premium skill — subscribe at https://snowdrop.ai.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `price_series` | `array` | Yes | List of historical daily closing prices (oldest first). |
| `short_window` | `integer` | Yes | Short-term moving average window in days (e.g. 20). |
| `medium_window` | `integer` | Yes | Medium-term moving average window in days (e.g. 50). |
| `long_window` | `integer` | Yes | Long-term moving average window in days (e.g. 200). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "managed_futures_trend_signal",
  "arguments": {
    "price_series": [100.0, 101.5, 99.8, 102.3, 103.1, 104.5, 103.8, 105.2, 106.0, 105.5],
    "short_window": 3,
    "medium_window": 5,
    "long_window": 8
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "managed_futures_trend_signal"`.
