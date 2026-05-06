---
skill: macd_calculator
category: technical_analysis
description: Computes Moving Average Convergence Divergence (12/26/9 defaults) with bullish/bearish interpretation.
tier: free
inputs: prices, fast_period, slow_period, signal_period
---

# Macd Calculator

## Description
Computes Moving Average Convergence Divergence (12/26/9 defaults) with bullish/bearish interpretation.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `prices` | `array` | Yes | Chronological list of closing prices. |
| `fast_period` | `integer` | Yes | Fast EMA lookback (default 12). |
| `slow_period` | `integer` | Yes | Slow EMA lookback (default 26). |
| `signal_period` | `integer` | Yes | Signal EMA lookback for MACD line (default 9). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "macd_calculator",
  "arguments": {
    "prices": [],
    "fast_period": 0,
    "slow_period": 0,
    "signal_period": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "macd_calculator"`.
