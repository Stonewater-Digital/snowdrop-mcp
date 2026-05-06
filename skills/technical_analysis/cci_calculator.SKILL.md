---
skill: cci_calculator
category: technical_analysis
description: Calculates Donald Lambert's Commodity Channel Index using a mean deviation normalization.
tier: free
inputs: highs, lows, closes, period, constant
---

# Cci Calculator

## Description
Calculates Donald Lambert's Commodity Channel Index using a mean deviation normalization.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `highs` | `array` | Yes | High prices. |
| `lows` | `array` | Yes | Low prices. |
| `closes` | `array` | Yes | Close prices. |
| `period` | `integer` | Yes | CCI period (default 20). |
| `constant` | `number` | Yes | Constant divisor (default 0.015). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "cci_calculator",
  "arguments": {
    "highs": [],
    "lows": [],
    "closes": [],
    "period": 0,
    "constant": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "cci_calculator"`.
