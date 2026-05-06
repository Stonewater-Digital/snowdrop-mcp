---
skill: annualized_return_calculator
category: portfolio
description: Converts a cumulative total return percentage into an annualized return using geometric compounding.
tier: free
inputs: total_return_pct, years
---

# Annualized Return Calculator

## Description
Converts a cumulative total return percentage into an annualized return using geometric compounding.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `total_return_pct` | `number` | Yes | Total return as a percentage (e.g. 50 for 50%). |
| `years` | `number` | Yes | Number of years over which the return was earned. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "annualized_return_calculator",
  "arguments": {
    "total_return_pct": 0,
    "years": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "annualized_return_calculator"`.
