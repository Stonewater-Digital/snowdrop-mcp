---
skill: etf_vs_mutual_fund_comparator
category: personal_finance
description: Aggregates expense ratios, commissions, and tax drag to compare ETF and mutual fund costs annually and across a 10-year horizon.
tier: free
inputs: investment_amount, etf_expense_ratio, mf_expense_ratio, etf_commission, trading_frequency, tax_bracket, turnover_rates
---

# Etf Vs Mutual Fund Comparator

## Description
Aggregates expense ratios, commissions, and tax drag to compare ETF and mutual fund costs annually and across a 10-year horizon.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `investment_amount` | `number` | Yes | Capital invested in dollars. |
| `etf_expense_ratio` | `number` | Yes | ETF annual expense ratio as decimal. |
| `mf_expense_ratio` | `number` | Yes | Mutual fund expense ratio as decimal. |
| `etf_commission` | `number` | Yes | Commission per ETF trade in dollars. |
| `trading_frequency` | `number` | Yes | Number of ETF trades per year. |
| `tax_bracket` | `number` | Yes | Marginal capital gains tax rate for distributions. |
| `turnover_rates` | `object` | Yes | Dictionary with 'etf' and 'mf' turnover assumptions (0-1). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "etf_vs_mutual_fund_comparator",
  "arguments": {
    "investment_amount": 0,
    "etf_expense_ratio": 0,
    "mf_expense_ratio": 0,
    "etf_commission": 0,
    "trading_frequency": 0,
    "tax_bracket": 0,
    "turnover_rates": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "etf_vs_mutual_fund_comparator"`.
