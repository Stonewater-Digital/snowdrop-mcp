---
skill: social_security_benefit_estimator
category: personal_finance
description: Estimate Social Security retirement benefits from average indexed monthly earnings (AIME). Calculates Primary Insurance Amount (PIA) and adjusts for early/late claiming.
tier: free
inputs: avg_monthly_earnings
---

# Social Security Benefit Estimator

## Description
Estimate Social Security retirement benefits from average indexed monthly earnings (AIME). Calculates Primary Insurance Amount (PIA) and adjusts for early/late claiming.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `avg_monthly_earnings` | `number` | Yes | Average Indexed Monthly Earnings (AIME). Can estimate as: (average annual earnings over best 35 years) / 12. |
| `full_retirement_age` | `integer` | No | Full retirement age (FRA). 67 for those born 1960+, 66 for earlier cohorts. |
| `claiming_age` | `integer` | No | Age at which benefits are claimed (62-70). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "social_security_benefit_estimator",
  "arguments": {
    "avg_monthly_earnings": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "social_security_benefit_estimator"`.
