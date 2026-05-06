---
skill: depreciation_units_of_production_calculator
category: accounting
description: Calculates depreciation using the units-of-production method, allocating cost based on actual units produced relative to total estimated output.
tier: free
inputs: cost, salvage_value, total_units, units_produced
---

# Depreciation Units Of Production Calculator

## Description
Calculates depreciation using the units-of-production method, allocating cost based on actual units produced relative to total estimated output.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `cost` | `number` | Yes | Original cost of the asset. |
| `salvage_value` | `number` | Yes | Estimated residual value at end of useful life. |
| `total_units` | `number` | Yes | Total estimated units the asset can produce over its life. |
| `units_produced` | `number` | Yes | Units actually produced in the current period. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "depreciation_units_of_production_calculator",
  "arguments": {
    "cost": 0,
    "salvage_value": 0,
    "total_units": 0,
    "units_produced": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "depreciation_units_of_production_calculator"`.
