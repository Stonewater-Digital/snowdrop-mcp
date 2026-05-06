---
skill: vwap_calculator
category: technical_analysis
description: Computes VWAP from typical price (H+L+C)/3 and derives 1/2 standard deviation bands.
tier: free
inputs: highs, lows, closes, volumes
---

# Vwap Calculator

## Description
Computes VWAP from typical price (H+L+C)/3 and derives 1/2 standard deviation bands.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `highs` | `array` | Yes | High prices. |
| `lows` | `array` | Yes | Low prices. |
| `closes` | `array` | Yes | Close prices. |
| `volumes` | `array` | Yes | Volume per bar. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "vwap_calculator",
  "arguments": {
    "highs": [],
    "lows": [],
    "closes": [],
    "volumes": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "vwap_calculator"`.
