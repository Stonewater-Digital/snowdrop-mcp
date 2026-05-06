---
skill: depreciation_sum_of_years_calculator
category: accounting
description: Calculates depreciation using the sum-of-the-years-digits method, returning a year-by-year schedule with declining depreciation amounts.
tier: free
inputs: cost, salvage_value, useful_life
---

# Depreciation Sum Of Years Calculator

## Description
Calculates depreciation using the sum-of-the-years-digits method, returning a year-by-year schedule with declining depreciation amounts.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `cost` | `number` | Yes | Original cost of the asset. |
| `salvage_value` | `number` | Yes | Estimated residual value at end of useful life. |
| `useful_life` | `integer` | Yes | Useful life of the asset in years (must be > 0). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "depreciation_sum_of_years_calculator",
  "arguments": {
    "cost": 0,
    "salvage_value": 0,
    "useful_life": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "depreciation_sum_of_years_calculator"`.
