---
skill: atr_calculator
category: technical_analysis
description: Implements Wilder's Average True Range for volatility assessment.
tier: free
inputs: highs, lows, closes, period
---

# Atr Calculator

## Description
Implements Wilder's Average True Range for volatility assessment.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `highs` | `array` | Yes | High prices. |
| `lows` | `array` | Yes | Low prices. |
| `closes` | `array` | Yes | Close prices. |
| `period` | `integer` | Yes | ATR period (default 14). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "atr_calculator",
  "arguments": {
    "highs": [],
    "lows": [],
    "closes": [],
    "period": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "atr_calculator"`.
