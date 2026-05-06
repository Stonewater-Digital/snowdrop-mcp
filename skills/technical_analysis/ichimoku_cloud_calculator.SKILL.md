---
skill: ichimoku_cloud_calculator
category: technical_analysis
description: Calculate all five Ichimoku Cloud components: Tenkan-sen, Kijun-sen, Senkou Span A, Senkou Span B, and Chikou Span.
tier: free
inputs: highs, lows, closes
---

# Ichimoku Cloud Calculator

## Description
Calculate all five Ichimoku Cloud components: Tenkan-sen, Kijun-sen, Senkou Span A, Senkou Span B, and Chikou Span.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `highs` | `array` | Yes | List of high prices (oldest to newest). |
| `lows` | `array` | Yes | List of low prices (oldest to newest). |
| `closes` | `array` | Yes | List of closing prices (oldest to newest). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "ichimoku_cloud_calculator",
  "arguments": {
    "highs": [],
    "lows": [],
    "closes": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "ichimoku_cloud_calculator"`.
