---
skill: auto_insurance_premium_estimator
category: insurance
description: Estimate auto insurance annual premium based on vehicle value, driver age, experience, accident history, and coverage type.
tier: free
inputs: vehicle_value, driver_age, years_licensed
---

# Auto Insurance Premium Estimator

## Description
Estimate auto insurance annual premium based on vehicle value, driver age, experience, accident history, and coverage type.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `vehicle_value` | `number` | Yes | Current vehicle value. |
| `driver_age` | `integer` | Yes | Driver's age. |
| `years_licensed` | `integer` | Yes | Years holding a valid license. |
| `accidents` | `integer` | No | Number of at-fault accidents in past 5 years (default 0). |
| `coverage_type` | `string` | No | Coverage type: 'full' (comprehensive+collision) or 'liability' (default 'full'). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "auto_insurance_premium_estimator",
  "arguments": {
    "vehicle_value": 0,
    "driver_age": 0,
    "years_licensed": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "auto_insurance_premium_estimator"`.
