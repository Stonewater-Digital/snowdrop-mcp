---
skill: funding_dilution_calculator
category: small_business
description: Walks through successive funding rounds to compute new share issuances, share prices, ownership percentages, and aggregate dilution for founders.
tier: free
inputs: rounds, founder_shares, option_pool_pct
---

# Funding Dilution Calculator

## Description
Walks through successive funding rounds to compute new share issuances, share prices, ownership percentages, and aggregate dilution for founders.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `rounds` | `array` | Yes | Funding rounds with name, pre_money_valuation, and investment_amount. |
| `founder_shares` | `number` | Yes | Outstanding founder shares prior to fundraising. |
| `option_pool_pct` | `number` | Yes | Option pool target as decimal percentage of post-money. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "funding_dilution_calculator",
  "arguments": {
    "rounds": [],
    "founder_shares": 0,
    "option_pool_pct": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "funding_dilution_calculator"`.
