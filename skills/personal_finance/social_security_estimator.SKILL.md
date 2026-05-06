---
skill: social_security_estimator
category: personal_finance
description: Approximates the primary insurance amount (PIA) and adjusts benefits for early or delayed claiming relative to full retirement age.
tier: free
inputs: average_indexed_monthly_earnings, birth_year, planned_claiming_age
---

# Social Security Estimator

## Description
Approximates the primary insurance amount (PIA) and adjusts benefits for early or delayed claiming relative to full retirement age.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `average_indexed_monthly_earnings` | `number` | Yes | Average indexed monthly earnings (AIME) in dollars. |
| `birth_year` | `number` | Yes | Birth year for FRA calculation. |
| `planned_claiming_age` | `number` | Yes | Age at which benefits will be claimed (62-70). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "social_security_estimator",
  "arguments": {
    "average_indexed_monthly_earnings": 0,
    "birth_year": 0,
    "planned_claiming_age": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "social_security_estimator"`.
