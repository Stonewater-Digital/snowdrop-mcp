---
skill: heikin_ashi_calculator
category: technical_analysis
description: Converts standard candles to Heikin-Ashi and reports trend direction and strength.
tier: free
inputs: opens, highs, lows, closes
---

# Heikin Ashi Calculator

## Description
Converts standard candles to Heikin-Ashi and reports trend direction and strength.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `opens` | `array` | Yes | Open prices. |
| `highs` | `array` | Yes | High prices. |
| `lows` | `array` | Yes | Low prices. |
| `closes` | `array` | Yes | Close prices. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "heikin_ashi_calculator",
  "arguments": {
    "opens": [],
    "highs": [],
    "lows": [],
    "closes": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "heikin_ashi_calculator"`.
