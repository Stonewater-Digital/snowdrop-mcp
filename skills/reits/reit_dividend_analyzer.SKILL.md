---
skill: reit_dividend_analyzer
category: reits
description: Evaluates dividend yield, payout ratios, and tax characterization.
tier: free
inputs: affo_per_share, dividend_per_share, share_price, taxable_income, total_distributions, return_of_capital_pct, capital_gain_pct, ordinary_income_pct
---

# Reit Dividend Analyzer

## Description
Evaluates dividend yield, payout ratios, and tax characterization.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `affo_per_share` | `number` | Yes |  |
| `dividend_per_share` | `number` | Yes |  |
| `share_price` | `number` | Yes |  |
| `taxable_income` | `number` | Yes |  |
| `total_distributions` | `number` | Yes |  |
| `return_of_capital_pct` | `number` | Yes |  |
| `capital_gain_pct` | `number` | Yes |  |
| `ordinary_income_pct` | `number` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "reit_dividend_analyzer",
  "arguments": {
    "affo_per_share": 0,
    "dividend_per_share": 0,
    "share_price": 0,
    "taxable_income": 0,
    "total_distributions": 0,
    "return_of_capital_pct": 0,
    "capital_gain_pct": 0,
    "ordinary_income_pct": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "reit_dividend_analyzer"`.
