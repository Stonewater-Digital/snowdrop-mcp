---
skill: margin_initial_simm
category: quantitative_risk
description: Approximates ISDA SIMM initial margin by aggregating weighted sensitivities per risk class.
tier: free
inputs: sensitivities
---

# Margin Initial Simm

## Description
Approximates ISDA SIMM initial margin by aggregating weighted sensitivities per risk class.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `sensitivities` | `array` | Yes | List of sensitivities (delta/vega) per risk class bucket. |
| `concentration_thresholds` | `object` | No | Threshold per risk class for concentration add-on. |
| `correlation` | `number` | No | Assumed correlation across buckets (default 0.5). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "margin_initial_simm",
  "arguments": {
    "sensitivities": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "margin_initial_simm"`.
