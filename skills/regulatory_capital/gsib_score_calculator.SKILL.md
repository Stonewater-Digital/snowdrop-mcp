---
skill: gsib_score_calculator
category: regulatory_capital
description: Computes Basel systemic importance score using indicator values and denominators.
tier: free
inputs: indicators, bucket_thresholds
---

# Gsib Score Calculator

## Description
Computes Basel systemic importance score using indicator values and denominators.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `indicators` | `array` | Yes | Indicator metrics with denominators and weights. |
| `bucket_thresholds` | `array` | Yes | List of score thresholds with surcharges. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "gsib_score_calculator",
  "arguments": {
    "indicators": [],
    "bucket_thresholds": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "gsib_score_calculator"`.
