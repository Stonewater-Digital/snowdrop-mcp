---
skill: health_insurance_plan_comparator
category: insurance
description: Compare health insurance plans by estimated total annual cost (premiums + out-of-pocket up to max) given expected medical costs. Ranks plans from cheapest to most expensive.
tier: free
inputs: plans, expected_costs
---

# Health Insurance Plan Comparator

## Description
Compare health insurance plans by estimated total annual cost (premiums + out-of-pocket up to max) given expected medical costs. Ranks plans from cheapest to most expensive.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `plans` | `array` | Yes | List of health insurance plans. |
| `expected_costs` | `number` | Yes | Expected annual medical costs before insurance. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "health_insurance_plan_comparator",
  "arguments": {
    "plans": [],
    "expected_costs": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "health_insurance_plan_comparator"`.
