---
skill: cohort_retention_analyzer
category: small_business
description: Computes retention percentages for each cohort, aggregates the average curve, and estimates cohort-level LTV along with churn by month.
tier: free
inputs: cohort_data
---

# Cohort Retention Analyzer

## Description
Computes retention percentages for each cohort, aggregates the average curve, and estimates cohort-level LTV along with churn by month.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `cohort_data` | `array` | Yes | List of cohorts with cohort_month and monthly_active_users series. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "cohort_retention_analyzer",
  "arguments": {
    "cohort_data": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "cohort_retention_analyzer"`.
