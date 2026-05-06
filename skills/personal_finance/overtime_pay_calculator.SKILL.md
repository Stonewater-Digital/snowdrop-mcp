---
skill: overtime_pay_calculator
category: personal_finance
description: Calculate overtime pay using hourly rate, regular hours, and overtime hours with configurable overtime multiplier (default 1.5x).
tier: free
inputs: hourly_rate
---

# Overtime Pay Calculator

## Description
Calculate overtime pay using hourly rate, regular hours, and overtime hours with configurable overtime multiplier (default 1.5x).

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `hourly_rate` | `number` | Yes | Regular hourly pay rate. |
| `regular_hours` | `number` | No | Number of regular (non-overtime) hours worked. |
| `overtime_hours` | `number` | No | Number of overtime hours worked. |
| `overtime_multiplier` | `number` | No | Overtime pay multiplier (1.5 = time and a half, 2.0 = double time). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "overtime_pay_calculator",
  "arguments": {
    "hourly_rate": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "overtime_pay_calculator"`.
