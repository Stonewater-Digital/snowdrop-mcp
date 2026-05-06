---
skill: revenue_per_employee_calculator
category: small_business
description: Calculate revenue per employee and compare against industry benchmarks.
tier: free
inputs: annual_revenue, num_employees
---

# Revenue Per Employee Calculator

## Description
Calculate revenue per employee and compare against industry benchmarks.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `annual_revenue` | `number` | Yes | Total annual revenue. |
| `num_employees` | `integer` | Yes | Number of full-time employees. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "revenue_per_employee_calculator",
  "arguments": {
    "annual_revenue": 0,
    "num_employees": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "revenue_per_employee_calculator"`.
