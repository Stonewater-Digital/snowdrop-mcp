---
skill: operational_risk_sma
category: quantitative_risk
description: Calculates SMA capital = BIC * ILM with Basel thresholds and loss component adjustments.
tier: free
inputs: business_indicator_components, internal_loss_history
---

# Operational Risk Sma

## Description
Calculates SMA capital = BIC * ILM with Basel thresholds and loss component adjustments.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `business_indicator_components` | `object` | Yes | Values for interest, service, and financial components (ILDC, SC, FC). |
| `ilm_scaling_factors` | `object` | No | Optional tuning for ILM formula constants. |
| `internal_loss_history` | `array` | Yes | Annual operational losses used for loss component (LC). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "operational_risk_sma",
  "arguments": {
    "business_indicator_components": {},
    "internal_loss_history": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "operational_risk_sma"`.
