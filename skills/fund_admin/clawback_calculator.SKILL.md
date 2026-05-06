---
skill: clawback_calculator
category: fund_admin
description: Determines GP clawback due when interim carried interest distributions exceed final entitlement. Optionally applies interest on the outstanding clawback amount.
tier: premium
inputs: carry_distributed, final_carry_entitlement, interest_rate_pct, years_outstanding, tax_rate_pct
---

# Clawback Calculator

## Description
Determines GP clawback due when interim carried interest distributions exceed final entitlement. Optionally applies interest on the outstanding clawback amount. (Premium — subscribe at https://snowdrop.ai)

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| carry_distributed | number | Yes | Total carried interest already distributed to the GP during the fund's life (USD) |
| final_carry_entitlement | number | Yes | GP's true carry entitlement based on final fund performance (USD) |
| interest_rate_pct | number | No | Annual interest rate applied to the clawback amount for the period it was held (default: 0.0) |
| years_outstanding | number | No | Number of years the excess carry was held before clawback is calculated (default: 0.0) |
| tax_rate_pct | number | No | Effective tax rate used to gross-up the clawback obligation (default: 0.0) |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "clawback_calculator",
  "arguments": {
    "carry_distributed": 4200000,
    "final_carry_entitlement": 3100000,
    "interest_rate_pct": 5.0,
    "years_outstanding": 3.0,
    "tax_rate_pct": 23.8
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "clawback_calculator"`.
