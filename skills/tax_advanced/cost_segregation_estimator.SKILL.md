---
skill: cost_segregation_estimator
category: tax_advanced
description: Approximates accelerated depreciation benefits from cost seg studies.
tier: free
inputs: building_cost, property_type, building_age_years
---

# Cost Segregation Estimator

## Description
Approximates accelerated depreciation benefits from cost seg studies.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `building_cost` | `number` | Yes |  |
| `property_type` | `string` | Yes |  |
| `building_age_years` | `integer` | Yes |  |
| `tax_rate` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "cost_segregation_estimator",
  "arguments": {
    "building_cost": 0,
    "property_type": "<property_type>",
    "building_age_years": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "cost_segregation_estimator"`.
