---
skill: balance_transfer_savings_calculator
category: banking
description: Calculate savings from transferring a credit card balance to a promotional APR. Accounts for transfer fee and compares interest saved.
tier: free
inputs: balance, current_apr, transfer_apr, transfer_fee_pct, promo_months
---

# Balance Transfer Savings Calculator

## Description
Calculate savings from transferring a credit card balance to a promotional APR. Accounts for transfer fee and compares interest saved.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `balance` | `number` | Yes | Current balance to transfer. |
| `current_apr` | `number` | Yes | Current card APR as decimal. |
| `transfer_apr` | `number` | Yes | Promotional APR as decimal (often 0). |
| `transfer_fee_pct` | `number` | Yes | Balance transfer fee as decimal (e.g., 0.03 for 3%). |
| `promo_months` | `integer` | Yes | Number of months at promotional rate. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "balance_transfer_savings_calculator",
  "arguments": {
    "balance": 0,
    "current_apr": 0,
    "transfer_apr": 0,
    "transfer_fee_pct": 0,
    "promo_months": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "balance_transfer_savings_calculator"`.
