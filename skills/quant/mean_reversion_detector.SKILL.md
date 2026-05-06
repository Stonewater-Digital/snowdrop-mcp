---
skill: mean_reversion_detector
category: quant
description: Estimates Ornstein-Uhlenbeck half-life and current deviation z-score via OLS regression.
tier: free
inputs: price_series
---

# Mean Reversion Detector

## Description
Estimates Ornstein-Uhlenbeck half-life and current deviation z-score via OLS regression.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `price_series` | `array` | Yes | Time-ordered price series (at least 10 observations recommended). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "mean_reversion_detector",
  "arguments": {
    "price_series": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "mean_reversion_detector"`.
