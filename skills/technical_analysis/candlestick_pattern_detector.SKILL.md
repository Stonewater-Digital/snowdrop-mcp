---
skill: candlestick_pattern_detector
category: technical_analysis
description: Scans OHLC data for common patterns: doji, hammer, engulfing, stars, soldiers/crows, harami, spinning top, shooting star.
tier: free
inputs: opens, highs, lows, closes
---

# Candlestick Pattern Detector

## Description
Scans OHLC data for common patterns: doji, hammer, engulfing, stars, soldiers/crows, harami, spinning top, shooting star.

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
  "tool": "candlestick_pattern_detector",
  "arguments": {
    "opens": [],
    "highs": [],
    "lows": [],
    "closes": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "candlestick_pattern_detector"`.
