---
skill: cd_yield_calculator
category: banking
description: Calculate CD maturity value and interest earned given principal, APY, and term in months.
tier: free
inputs: principal, apy, term_months
---

# Cd Yield Calculator

## Description
Calculate CD maturity value and interest earned given principal, APY, and term in months.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `principal` | `number` | Yes | Initial deposit amount. |
| `apy` | `number` | Yes | Annual Percentage Yield as a decimal (e.g., 0.045 for 4.5%). |
| `term_months` | `integer` | Yes | CD term length in months. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "cd_yield_calculator",
  "arguments": {
    "principal": 0,
    "apy": 0,
    "term_months": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "cd_yield_calculator"`.
