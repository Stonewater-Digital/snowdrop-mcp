---
skill: dry_powder_calculator
category: fund_accounting
description: Calculates available dry powder (uninvested capital), deployment rate, and deployment runway for a private equity fund. Dry powder = total_commitments - capital_called - reserves.
tier: premium
inputs: total_commitments, capital_called, reserves, monthly_deployment_rate
---

# Dry Powder Calculator

## Description
Calculates available dry powder (uninvested capital), deployment rate, and deployment runway for a private equity fund. Dry powder = total_commitments - capital_called - reserves. If monthly_deployment_rate is provided, runway_months = dry_powder / rate. Useful for fund pacing, LP reporting, and GP investment planning. Premium skill — subscribe at https://snowdrop.ai.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `total_commitments` | `number` | Yes | Total LP capital commitments to the fund in dollars. |
| `capital_called` | `number` | Yes | Capital already drawn down from LPs to date in dollars. |
| `reserves` | `number` | Yes | Capital set aside for follow-on investments and fund expenses in dollars. |
| `monthly_deployment_rate` | `number` | No | Average monthly capital deployment rate in dollars. If provided, calculates deployment runway in months. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "dry_powder_calculator",
  "arguments": {
    "total_commitments": 100000000,
    "capital_called": 55000000,
    "reserves": 5000000,
    "monthly_deployment_rate": 3000000
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "dry_powder_calculator"`.
