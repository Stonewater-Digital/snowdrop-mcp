---
skill: chaikin_money_flow_calculator
category: technical_analysis
description: Calculate Chaikin Money Flow (CMF), which measures the accumulation/distribution of money flow over a period. Positive CMF = buying pressure, negative = selling pressure.
tier: free
inputs: highs, lows, closes, volumes
---

# Chaikin Money Flow Calculator

## Description
Calculate Chaikin Money Flow (CMF), which measures the accumulation/distribution of money flow over a period. Positive CMF = buying pressure, negative = selling pressure.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `highs` | `array` | Yes | List of high prices (oldest to newest). |
| `lows` | `array` | Yes | List of low prices (oldest to newest). |
| `closes` | `array` | Yes | List of closing prices (oldest to newest). |
| `volumes` | `array` | Yes | List of volume values (oldest to newest). |
| `period` | `integer` | No | CMF lookback period. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "chaikin_money_flow_calculator",
  "arguments": {
    "highs": [],
    "lows": [],
    "closes": [],
    "volumes": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "chaikin_money_flow_calculator"`.
