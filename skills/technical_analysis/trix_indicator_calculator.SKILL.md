---
skill: trix_indicator_calculator
category: technical_analysis
description: Calculate the TRIX indicator, a momentum oscillator based on the rate of change of a triple-smoothed EMA. Filters out insignificant price movements.
tier: free
inputs: closes
---

# Trix Indicator Calculator

## Description
Calculate the TRIX indicator, a momentum oscillator based on the rate of change of a triple-smoothed EMA. Filters out insignificant price movements.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `closes` | `array` | Yes | List of closing prices (oldest to newest). |
| `period` | `integer` | No | EMA period for each of the three smoothings. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "trix_indicator_calculator",
  "arguments": {
    "closes": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "trix_indicator_calculator"`.
