---
skill: reit_dividend_tax_treatment_analyzer
category: securities_tax
description: Allocates REIT dividends into tax character categories and rates.
tier: free
inputs: dividend_amount, ordinary_pct, capital_gain_pct, roc_pct
---

# Reit Dividend Tax Treatment Analyzer

## Description
Allocates REIT dividends into tax character categories and rates.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `dividend_amount` | `number` | Yes |  |
| `ordinary_pct` | `number` | Yes |  |
| `capital_gain_pct` | `number` | Yes |  |
| `roc_pct` | `number` | Yes |  |
| `ordinary_rate_pct` | `number` | No |  |
| `capital_gain_rate_pct` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "reit_dividend_tax_treatment_analyzer",
  "arguments": {
    "dividend_amount": 0,
    "ordinary_pct": 0,
    "capital_gain_pct": 0,
    "roc_pct": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "reit_dividend_tax_treatment_analyzer"`.
