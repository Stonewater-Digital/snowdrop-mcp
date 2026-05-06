---
skill: market_risk_frtb_sa
category: quantitative_risk
description: Computes delta/vega/curvature buckets with prescribed correlations to derive FRTB SA capital plus DRC add-on.
tier: free
inputs: sensitivities, correlation_scenarios
---

# Market Risk Frtb Sa

## Description
Computes delta/vega/curvature buckets with prescribed correlations to derive FRTB SA capital plus DRC add-on.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `sensitivities` | `array` | Yes | Per risk class sensitivities with Basel risk weights. |
| `correlation_scenarios` | `object` | Yes | Correlation parameter rho for low/medium/high stress calibration. |
| `drc_addon` | `number` | No | Default risk capital add-on in base currency. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "market_risk_frtb_sa",
  "arguments": {
    "sensitivities": [],
    "correlation_scenarios": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "market_risk_frtb_sa"`.
