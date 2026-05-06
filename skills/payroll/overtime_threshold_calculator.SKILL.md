---
skill: overtime_threshold_calculator
category: payroll
description: Calculate regular and overtime pay given hourly rate, hours worked, overtime multiplier, and threshold (default 40 hours).
tier: free
inputs: hourly_rate, hours_worked
---

# Overtime Threshold Calculator

## Description
Calculate regular and overtime pay given hourly rate, hours worked, overtime multiplier, and threshold (default 40 hours).

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `hourly_rate` | `number` | Yes | Regular hourly rate in USD. |
| `hours_worked` | `number` | Yes | Total hours worked in the period. |
| `overtime_multiplier` | `number` | No | Overtime pay multiplier (e.g. 1.5 for time-and-a-half). |
| `threshold` | `number` | No | Hours threshold before overtime kicks in. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "overtime_threshold_calculator",
  "arguments": {
    "hourly_rate": 22.50,
    "hours_worked": 46
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "overtime_threshold_calculator"`.
