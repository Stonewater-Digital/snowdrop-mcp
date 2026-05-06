---
skill: coast_fire_calculator
category: budgeting
description: Determines if current savings will compound to the target retirement amount without additional contributions (Coast FIRE).
tier: free
inputs: current_savings, target_amount, years_to_retire
---

# Coast Fire Calculator

## Description
Determines if current savings will compound to the target retirement amount without additional contributions (Coast FIRE).

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `current_savings` | `number` | Yes | Current total invested savings in dollars. |
| `target_amount` | `number` | Yes | Target retirement portfolio amount in dollars. |
| `years_to_retire` | `number` | Yes | Number of years until planned retirement. |
| `expected_return` | `number` | No | Expected annual real investment return as a decimal (default: 0.07). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "coast_fire_calculator",
  "arguments": {
    "current_savings": 0,
    "target_amount": 0,
    "years_to_retire": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "coast_fire_calculator"`.
