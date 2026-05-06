---
skill: depreciation_calculator
category: small_business
description: Produces annual depreciation schedules for straight-line, declining balance, MACRS (simplified), and sum-of-years methods.
tier: free
inputs: asset_cost, salvage_value, useful_life_years, method
---

# Depreciation Calculator

## Description
Produces annual depreciation schedules for straight-line, declining balance, MACRS (simplified), and sum-of-years methods.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `asset_cost` | `number` | Yes | Original asset cost. |
| `salvage_value` | `number` | Yes | Residual value at end of life. |
| `useful_life_years` | `number` | Yes | Asset useful life in years. |
| `method` | `string` | Yes | Depreciation method: straight_line, declining_balance, macrs, or sum_of_years. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "depreciation_calculator",
  "arguments": {
    "asset_cost": 0,
    "salvage_value": 0,
    "useful_life_years": 0,
    "method": "<method>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "depreciation_calculator"`.
