---
skill: chaikin_volatility
category: technical_analysis
description: Calculates Chaikin Volatility (EMA of range with rate-of-change comparison).
tier: free
inputs: highs, lows, ema_period, roc_period
---

# Chaikin Volatility

## Description
Calculates Chaikin Volatility (EMA of range with rate-of-change comparison).

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `highs` | `array` | Yes | High prices. |
| `lows` | `array` | Yes | Low prices. |
| `ema_period` | `integer` | Yes | EMA period (default 10). |
| `roc_period` | `integer` | Yes | Lookback for EMA rate-of-change (default 10). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "chaikin_volatility",
  "arguments": {
    "highs": [],
    "lows": [],
    "ema_period": 0,
    "roc_period": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "chaikin_volatility"`.
