---
skill: key_person_insurance_valuation
category: corporate_insurance
description: Calculates key person insurance amount using salary, pipeline, and replacement time.
tier: free
inputs: annual_compensation, revenue_contribution, replacement_time_months
---

# Key Person Insurance Valuation

## Description
Calculates key person insurance amount using salary, pipeline, and replacement time.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `annual_compensation` | `number` | Yes |  |
| `revenue_contribution` | `number` | Yes |  |
| `replacement_time_months` | `number` | Yes |  |
| `knowledge_transfer_factor_pct` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "key_person_insurance_valuation",
  "arguments": {
    "annual_compensation": 0,
    "revenue_contribution": 0,
    "replacement_time_months": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "key_person_insurance_valuation"`.
