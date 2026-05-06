---
skill: calmar_ratio_calculator
category: portfolio
description: Calculates the Calmar ratio, comparing annualized return to maximum drawdown as a measure of risk-adjusted performance.
tier: free
inputs: annual_return, max_drawdown
---

# Calmar Ratio Calculator

## Description
Calculates the Calmar ratio, comparing annualized return to maximum drawdown as a measure of risk-adjusted performance.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `annual_return` | `number` | Yes | Annualized return (decimal, e.g. 0.12 for 12%). |
| `max_drawdown` | `number` | Yes | Maximum drawdown as a positive decimal (e.g. 0.20 for 20%). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "calmar_ratio_calculator",
  "arguments": {
    "annual_return": 0,
    "max_drawdown": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "calmar_ratio_calculator"`.
