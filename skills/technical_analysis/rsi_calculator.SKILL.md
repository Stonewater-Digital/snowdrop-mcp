---
skill: rsi_calculator
category: technical_analysis
description: Computes RSI using J. Welles Wilder's smoothing to spot overbought or oversold conditions.
tier: free
inputs: prices, period
---

# Rsi Calculator

## Description
Computes RSI using J. Welles Wilder's smoothing to spot overbought or oversold conditions.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `prices` | `array` | Yes | Close prices (oldest first). |
| `period` | `integer` | Yes | RSI lookback period (default 14). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "rsi_calculator",
  "arguments": {
    "prices": [],
    "period": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rsi_calculator"`.
