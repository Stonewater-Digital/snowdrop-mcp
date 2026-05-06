---
skill: deductible_optimization_calculator
category: insurance
description: Compare low vs high deductible plans: premium savings, breakeven claims needed, and expected value analysis.
tier: free
inputs: low_deductible, low_premium, high_deductible, high_premium
---

# Deductible Optimization Calculator

## Description
Compare low vs high deductible plans: premium savings, breakeven claims needed, and expected value analysis.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `low_deductible` | `number` | Yes | Low deductible amount. |
| `low_premium` | `number` | Yes | Monthly premium for low-deductible plan. |
| `high_deductible` | `number` | Yes | High deductible amount. |
| `high_premium` | `number` | Yes | Monthly premium for high-deductible plan. |
| `expected_claims_per_year` | `number` | No | Expected number of claims per year (default 0.5). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "deductible_optimization_calculator",
  "arguments": {
    "low_deductible": 0,
    "low_premium": 0,
    "high_deductible": 0,
    "high_premium": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "deductible_optimization_calculator"`.
