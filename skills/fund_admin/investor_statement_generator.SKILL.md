---
skill: investor_statement_generator
category: fund_admin
description: Builds LP investor statement data including NAV, DPI, TVPI, RVPI, unfunded commitment, and IRR. Validates that called capital does not exceed commitment.
tier: premium
inputs: lp_name, commitment, capital_called, distributions, nav, irr_pct
---

# Investor Statement Generator

## Description
Builds LP investor statement data including NAV, DPI, TVPI, RVPI, unfunded commitment, and IRR. Validates that called capital does not exceed commitment. (Premium — subscribe at https://snowdrop.ai)

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| lp_name | string | Yes | Legal name of the limited partner as it appears on the subscription agreement |
| commitment | number | Yes | Total LP commitment to the fund (USD) |
| capital_called | number | Yes | Cumulative capital drawn from the LP to date (USD) |
| distributions | number | Yes | Cumulative cash distributions returned to the LP to date (USD) |
| nav | number | Yes | LP's current net asset value (residual fair value of their interest, USD) |
| irr_pct | number | No | LP's net IRR as a percentage for inclusion in the statement (default: 0.0) |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "investor_statement_generator",
  "arguments": {
    "lp_name": "Great Lakes Pension Fund LLC",
    "commitment": 15000000,
    "capital_called": 9750000,
    "distributions": 4200000,
    "nav": 8100000,
    "irr_pct": 13.7
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "investor_statement_generator"`.
