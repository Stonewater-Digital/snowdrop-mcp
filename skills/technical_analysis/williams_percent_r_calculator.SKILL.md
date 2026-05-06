---
skill: williams_percent_r_calculator
category: technical_analysis
description: Calculate Williams %R, a momentum oscillator ranging from -100 to 0. Readings above -20 are overbought; below -80 are oversold.
tier: free
inputs: highs, lows, closes
---

# Williams Percent R Calculator

## Description
Calculate Williams %R, a momentum oscillator ranging from -100 to 0. Readings above -20 are overbought; below -80 are oversold.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `highs` | `array` | Yes | List of high prices (oldest to newest). |
| `lows` | `array` | Yes | List of low prices (oldest to newest). |
| `closes` | `array` | Yes | List of closing prices (oldest to newest). |
| `period` | `integer` | No | Lookback period. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "williams_percent_r_calculator",
  "arguments": {
    "highs": [],
    "lows": [],
    "closes": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "williams_percent_r_calculator"`.
