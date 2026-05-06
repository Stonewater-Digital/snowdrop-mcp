---
skill: momentum_oscillator
category: technical_analysis
description: Measures price momentum as the difference and percent change over a configurable lookback.
tier: free
inputs: prices, period
---

# Momentum Oscillator

## Description
Measures price momentum as the difference and percent change over a configurable lookback.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `prices` | `array` | Yes | Price list (oldest first). |
| `period` | `integer` | Yes | Lookback period for momentum calculation. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "momentum_oscillator",
  "arguments": {
    "prices": [],
    "period": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "momentum_oscillator"`.
