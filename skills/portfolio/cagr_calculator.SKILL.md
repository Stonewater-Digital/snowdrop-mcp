---
skill: cagr_calculator
category: portfolio
description: Calculates the compound annual growth rate (CAGR), the geometric average annual return between a beginning and ending value.
tier: free
inputs: begin_value, end_value, years
---

# Cagr Calculator

## Description
Calculates the compound annual growth rate (CAGR), the geometric average annual return between a beginning and ending value.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `begin_value` | `number` | Yes | Beginning value of the investment. |
| `end_value` | `number` | Yes | Ending value of the investment. |
| `years` | `number` | Yes | Number of years over which growth occurred. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "cagr_calculator",
  "arguments": {
    "begin_value": 0,
    "end_value": 0,
    "years": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "cagr_calculator"`.
