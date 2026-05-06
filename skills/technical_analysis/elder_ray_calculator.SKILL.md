---
skill: elder_ray_calculator
category: technical_analysis
description: Calculate Elder Ray Index with Bull Power (High - EMA) and Bear Power (Low - EMA). Used to measure buying and selling pressure relative to the trend.
tier: free
inputs: highs, lows, closes
---

# Elder Ray Calculator

## Description
Calculate Elder Ray Index with Bull Power (High - EMA) and Bear Power (Low - EMA). Used to measure buying and selling pressure relative to the trend.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `highs` | `array` | Yes | List of high prices (oldest to newest). |
| `lows` | `array` | Yes | List of low prices (oldest to newest). |
| `closes` | `array` | Yes | List of closing prices (oldest to newest). |
| `period` | `integer` | No | EMA period for the Elder Ray calculation. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "elder_ray_calculator",
  "arguments": {
    "highs": [],
    "lows": [],
    "closes": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "elder_ray_calculator"`.
