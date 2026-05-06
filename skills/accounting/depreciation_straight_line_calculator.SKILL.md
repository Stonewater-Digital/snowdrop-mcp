---
skill: depreciation_straight_line_calculator
category: accounting
description: Calculates annual depreciation expense using the straight-line method, returning per-year depreciation and a full schedule.
tier: free
inputs: cost, salvage_value, useful_life
---

# Depreciation Straight Line Calculator

## Description
Calculates annual depreciation expense using the straight-line method, returning per-year depreciation and a full schedule.

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
  "tool": "depreciation_straight_line_calculator",
  "arguments": {
    "cost": 0,
    "salvage_value": 0,
    "useful_life": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "depreciation_straight_line_calculator"`.
