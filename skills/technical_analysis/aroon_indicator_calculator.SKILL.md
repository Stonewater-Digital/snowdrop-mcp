---
skill: aroon_indicator_calculator
category: technical_analysis
description: Calculate the Aroon indicator (Aroon Up and Aroon Down), which identifies trend strength and direction based on the time since the highest high and lowest low.
tier: free
inputs: highs, lows
---

# Aroon Indicator Calculator

## Description
Calculate the Aroon indicator (Aroon Up and Aroon Down), which identifies trend strength and direction based on the time since the highest high and lowest low.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `highs` | `array` | Yes | List of high prices (oldest to newest). |
| `lows` | `array` | Yes | List of low prices (oldest to newest). |
| `period` | `integer` | No | Aroon lookback period. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "aroon_indicator_calculator",
  "arguments": {
    "highs": [],
    "lows": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "aroon_indicator_calculator"`.
