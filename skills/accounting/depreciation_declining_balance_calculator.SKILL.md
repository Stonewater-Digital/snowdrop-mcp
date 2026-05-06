---
skill: depreciation_declining_balance_calculator
category: accounting
description: Calculates depreciation using the declining-balance method (default double declining). Returns a year-by-year schedule clamped to salvage value.
tier: free
inputs: cost, salvage_value, useful_life
---

# Depreciation Declining Balance Calculator

## Description
Calculates depreciation using the declining-balance method (default double declining). Returns a year-by-year schedule clamped to salvage value.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `cost` | `number` | Yes | Original cost of the asset. |
| `salvage_value` | `number` | Yes | Estimated residual value at end of useful life. |
| `useful_life` | `integer` | Yes | Useful life of the asset in years (must be > 0). |
| `factor` | `number` | No | Acceleration factor (default 2.0 for double-declining). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "depreciation_declining_balance_calculator",
  "arguments": {
    "cost": 0,
    "salvage_value": 0,
    "useful_life": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "depreciation_declining_balance_calculator"`.
