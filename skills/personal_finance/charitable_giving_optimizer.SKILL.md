---
skill: charitable_giving_optimizer
category: personal_finance
description: Applies IRS AGI limits for cash (60%) and appreciated asset (30%) donations and advises whether gifting stock yields higher tax savings.
tier: free
inputs: cash_donations, appreciated_assets, agi, filing_status
---

# Charitable Giving Optimizer

## Description
Applies IRS AGI limits for cash (60%) and appreciated asset (30%) donations and advises whether gifting stock yields higher tax savings.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `cash_donations` | `number` | Yes | Planned cash contributions to qualified charities. |
| `appreciated_assets` | `array` | Yes | List of assets with fmv, cost_basis, holding_period (months). |
| `agi` | `number` | Yes | Adjusted gross income for the tax year. |
| `filing_status` | `string` | Yes | single or mfj. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "charitable_giving_optimizer",
  "arguments": {
    "cash_donations": 0,
    "appreciated_assets": [],
    "agi": 0,
    "filing_status": "<filing_status>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "charitable_giving_optimizer"`.
