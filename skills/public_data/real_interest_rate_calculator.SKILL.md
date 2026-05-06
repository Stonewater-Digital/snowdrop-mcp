---
skill: real_interest_rate_calculator
category: public_data
description: Calculate the real interest rate from nominal rate and inflation using the Fisher equation. Returns both exact and approximate values.
tier: free
inputs: nominal_rate, inflation_rate
---

# Real Interest Rate Calculator

## Description
Calculate the real interest rate from nominal rate and inflation using the Fisher equation. Returns both exact and approximate values.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `nominal_rate` | `number` | Yes | Nominal interest rate as a decimal (e.g., 0.05 for 5%). |
| `inflation_rate` | `number` | Yes | Inflation rate as a decimal (e.g., 0.03 for 3%). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "real_interest_rate_calculator",
  "arguments": {
    "nominal_rate": 0,
    "inflation_rate": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "real_interest_rate_calculator"`.
