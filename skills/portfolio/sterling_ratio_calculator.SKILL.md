---
skill: sterling_ratio_calculator
category: portfolio
description: Calculates the Sterling ratio, comparing annualized return to average maximum drawdown plus a 10% buffer.
tier: free
inputs: annual_return, avg_max_drawdown
---

# Sterling Ratio Calculator

## Description
Calculates the Sterling ratio, comparing annualized return to average maximum drawdown plus a 10% buffer.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `annual_return` | `number` | Yes | Annualized return (decimal, e.g. 0.15 for 15%). |
| `avg_max_drawdown` | `number` | Yes | Average maximum drawdown as a positive decimal. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "sterling_ratio_calculator",
  "arguments": {
    "annual_return": 0,
    "avg_max_drawdown": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "sterling_ratio_calculator"`.
