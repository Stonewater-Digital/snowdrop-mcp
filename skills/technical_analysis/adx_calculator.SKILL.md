---
skill: adx_calculator
category: technical_analysis
description: Applies Wilder's Average Directional Index to gauge whether trends are weak or strong.
tier: free
inputs: highs, lows, closes, period
---

# Adx Calculator

## Description
Applies Wilder's Average Directional Index to gauge whether trends are weak or strong.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `highs` | `array` | Yes | High prices (oldest first). |
| `lows` | `array` | Yes | Low prices aligned with highs. |
| `closes` | `array` | Yes | Close prices for true range computation. |
| `period` | `integer` | Yes | ADX period, typically 14. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "adx_calculator",
  "arguments": {
    "highs": [],
    "lows": [],
    "closes": [],
    "period": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "adx_calculator"`.
