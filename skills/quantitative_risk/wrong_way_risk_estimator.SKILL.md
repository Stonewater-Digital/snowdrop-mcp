---
skill: wrong_way_risk_estimator
category: quantitative_risk
description: Applies a correlation-driven multiplier to CVA following Basel/WP80 guidance on wrong-way risk.
tier: free
inputs: counterparty_pd, exposure_at_default, correlation
---

# Wrong Way Risk Estimator

## Description
Applies a correlation-driven multiplier to CVA following Basel/WP80 guidance on wrong-way risk.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `counterparty_pd` | `number` | Yes | Counterparty one-year probability of default (0-1). |
| `exposure_at_default` | `number` | Yes | Exposure at default (EAD) in base currency. |
| `correlation` | `number` | Yes | Correlation between EAD and PD derived from stress testing. |
| `lgd_pct` | `number` | No | Loss-given-default percentage (0-100). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "wrong_way_risk_estimator",
  "arguments": {
    "counterparty_pd": 0,
    "exposure_at_default": 0,
    "correlation": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "wrong_way_risk_estimator"`.
