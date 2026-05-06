---
skill: cyber_insurance_exposure_estimator
category: corporate_insurance
description: Estimates cyber limit need from revenue, records, and controls maturity.
tier: free
inputs: annual_revenue, records_at_risk_millions, control_score_pct, event_probability_pct
---

# Cyber Insurance Exposure Estimator

## Description
Estimates cyber limit need from revenue, records, and controls maturity.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `annual_revenue` | `number` | Yes |  |
| `records_at_risk_millions` | `number` | Yes |  |
| `control_score_pct` | `number` | Yes |  |
| `event_probability_pct` | `number` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "cyber_insurance_exposure_estimator",
  "arguments": {
    "annual_revenue": 0,
    "records_at_risk_millions": 0,
    "control_score_pct": 0,
    "event_probability_pct": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "cyber_insurance_exposure_estimator"`.
