---
skill: conditional_var_calculator
category: portfolio
description: Calculates Conditional Value at Risk (CVaR), also known as Expected Shortfall, the average loss beyond the VaR threshold.
tier: free
inputs: returns
---

# Conditional Var Calculator

## Description
Calculates Conditional Value at Risk (CVaR), also known as Expected Shortfall, the average loss beyond the VaR threshold.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `returns` | `array` | Yes | List of periodic returns as decimals. |
| `confidence` | `number` | No | Confidence level (default 0.95 for 95%). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "conditional_var_calculator",
  "arguments": {
    "returns": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "conditional_var_calculator"`.
