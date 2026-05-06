---
skill: gp_co_invest_calculator
category: fund_admin
description: Calculates GP and LP capital allocations plus promote economics for co-investment deals. Returns GP commitment, LP commitment, and the promote pool available for the GP.
tier: premium
inputs: deal_equity, gp_commit_pct, promote_pct
---

# Gp Co Invest Calculator

## Description
Calculates GP and LP capital allocations plus promote economics for co-investment deals. Returns GP commitment, LP commitment, and the promote pool available for the GP. (Premium — subscribe at https://snowdrop.ai)

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| deal_equity | number | Yes | Total equity capital required for the co-investment deal (USD) |
| gp_commit_pct | number | Yes | GP's equity contribution as a percentage of total deal equity (e.g. 5.0 for 5%) |
| promote_pct | number | No | GP promote (carried interest) percentage on LP profits above cost in the co-invest vehicle (default: 20.0) |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "gp_co_invest_calculator",
  "arguments": {
    "deal_equity": 50000000,
    "gp_commit_pct": 5.0,
    "promote_pct": 20.0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "gp_co_invest_calculator"`.
