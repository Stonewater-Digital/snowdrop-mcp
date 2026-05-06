---
skill: carried_interest_tax_analyzer
category: fund_tax
description: Calculates tax liability for carried interest under three-year rule. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: carried_interest, holding_period_years
---

# Carried Interest Tax Analyzer

## Description
Calculates tax liability for carried interest under three-year rule. (Premium — subscribe at https://snowdrop.ai)

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `carried_interest` | `number` | Yes | Dollar value of the carried interest allocation being evaluated under IRC §1061 |
| `holding_period_years` | `number` | Yes | Holding period in years — determines short-term (<3 years) vs long-term recharacterization |
| `capital_gains_rate_pct` | `number` | No | Applicable long-term capital gains rate (default: 20.0) |
| `ordinary_rate_pct` | `number` | No | Applicable ordinary income tax rate for short-term recharacterization (default: 37.0) |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "carried_interest_tax_analyzer",
  "arguments": {
    "carried_interest": 2500000.00,
    "holding_period_years": 2.5,
    "capital_gains_rate_pct": 20.0,
    "ordinary_rate_pct": 37.0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "carried_interest_tax_analyzer"`.
