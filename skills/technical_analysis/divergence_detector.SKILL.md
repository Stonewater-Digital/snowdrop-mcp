---
skill: divergence_detector
category: technical_analysis
description: Identifies regular and hidden divergences between price action and an oscillator/indicator.
tier: free
inputs: prices, indicator_values, lookback
---

# Divergence Detector

## Description
Identifies regular and hidden divergences between price action and an oscillator/indicator.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `prices` | `array` | Yes | Price series. |
| `indicator_values` | `array` | Yes | Indicator series aligned with prices. |
| `lookback` | `integer` | Yes | Window used to search for pivots. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "divergence_detector",
  "arguments": {
    "prices": [],
    "indicator_values": [],
    "lookback": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "divergence_detector"`.
