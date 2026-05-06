---
skill: parabolic_sar_calculator
category: technical_analysis
description: Calculate the Parabolic SAR (Stop and Reverse) indicator. Used for trailing stop placement and trend direction identification.
tier: free
inputs: highs, lows
---

# Parabolic Sar Calculator

## Description
Calculate the Parabolic SAR (Stop and Reverse) indicator. Used for trailing stop placement and trend direction identification.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `highs` | `array` | Yes | List of high prices (oldest to newest). |
| `lows` | `array` | Yes | List of low prices (oldest to newest). |
| `af_start` | `number` | No | Initial acceleration factor. |
| `af_max` | `number` | No | Maximum acceleration factor. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "parabolic_sar_calculator",
  "arguments": {
    "highs": [],
    "lows": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "parabolic_sar_calculator"`.
