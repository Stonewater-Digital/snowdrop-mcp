---
skill: credit_waterfall_calculator
category: private_credit
description: Allocates cash to fees, senior, mezzanine, and equity tranches.
tier: free
inputs: cash_available, fee_amount, senior_outstanding, mezz_outstanding
---

# Credit Waterfall Calculator

## Description
Allocates cash to fees, senior, mezzanine, and equity tranches.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `cash_available` | `number` | Yes |  |
| `fee_amount` | `number` | Yes |  |
| `senior_outstanding` | `number` | Yes |  |
| `mezz_outstanding` | `number` | Yes |  |
| `equity_share_pct` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "credit_waterfall_calculator",
  "arguments": {
    "cash_available": 0,
    "fee_amount": 0,
    "senior_outstanding": 0,
    "mezz_outstanding": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "credit_waterfall_calculator"`.
