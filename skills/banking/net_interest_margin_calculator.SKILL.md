---
skill: net_interest_margin_calculator
category: banking
description: Computes current NIM, gap ratios, and projected NIM under rate shocks.
tier: free
inputs: interest_income, interest_expense, earning_assets, rate_environment, asset_repricing_pct, liability_repricing_pct
---

# Net Interest Margin Calculator

## Description
Computes current NIM, gap ratios, and projected NIM under rate shocks.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `interest_income` | `number` | Yes |  |
| `interest_expense` | `number` | Yes |  |
| `earning_assets` | `number` | Yes |  |
| `rate_environment` | `string` | Yes |  |
| `asset_repricing_pct` | `number` | Yes |  |
| `liability_repricing_pct` | `number` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "net_interest_margin_calculator",
  "arguments": {
    "interest_income": 0,
    "interest_expense": 0,
    "earning_assets": 0,
    "rate_environment": "<rate_environment>",
    "asset_repricing_pct": 0,
    "liability_repricing_pct": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "net_interest_margin_calculator"`.
