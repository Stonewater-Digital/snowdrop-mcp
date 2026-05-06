---
skill: disability_insurance_estimator
category: insurance
description: Estimate disability insurance monthly benefit needs (typically 60% of income) and calculate any coverage gap.
tier: free
inputs: monthly_income
---

# Disability Insurance Estimator

## Description
Estimate disability insurance monthly benefit needs (typically 60% of income) and calculate any coverage gap.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `monthly_income` | `number` | Yes | Gross monthly income. |
| `coverage_pct` | `number` | No | Desired coverage as decimal (default 0.60 for 60%). |
| `existing_coverage` | `number` | No | Existing monthly disability benefit (default 0). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "disability_insurance_estimator",
  "arguments": {
    "monthly_income": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "disability_insurance_estimator"`.
