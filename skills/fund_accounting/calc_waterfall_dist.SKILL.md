---
skill: calc_waterfall_dist
category: fund_accounting
description: Calculates LP/GP waterfall distributions across preferred return, catch-up, and carried interest tiers. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: fund_size, preferred_return, carry_rate, gp_commitment, distribution_amount
---

# Calc Waterfall Dist

## Description
Calculates LP/GP waterfall distributions across preferred return, catch-up, and carried interest tiers. Models the standard American/European waterfall: (1) return of capital, (2) preferred return to LPs, (3) GP catch-up, (4) carried interest split. Premium skill — subscribe at https://snowdrop.ai.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `fund_size` | `number` | Yes | Total fund size (total LP + GP commitments) in dollars. |
| `preferred_return` | `number` | Yes | Preferred return rate (hurdle rate), e.g. 0.08 for 8%. |
| `carry_rate` | `number` | Yes | GP carried interest rate, e.g. 0.20 for 20%. |
| `gp_commitment` | `number` | Yes | GP commitment amount in dollars. |
| `distribution_amount` | `number` | Yes | Total proceeds available for distribution in dollars. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "calc_waterfall_dist",
  "arguments": {
    "fund_size": 100000000,
    "preferred_return": 0.08,
    "carry_rate": 0.20,
    "gp_commitment": 2000000,
    "distribution_amount": 150000000
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "calc_waterfall_dist"`.
