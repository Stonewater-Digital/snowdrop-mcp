---
skill: regime_detector
category: quant
description: Detects bull vs bear regimes using realized volatility and return trends.
tier: free
inputs: return_series
---

# Regime Detector

## Description
Detects bull vs bear regimes using realized volatility and return trends.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `return_series` | `array` | Yes |  |
| `vol_window` | `integer` | No |  |
| `vol_threshold_pct` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "regime_detector",
  "arguments": {
    "return_series": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "regime_detector"`.
