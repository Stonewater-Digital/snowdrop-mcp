---
skill: high_yield_savings_comparator
category: personal_finance
description: Compares multiple savings accounts by incorporating APY, minimum balances, and monthly fees to surface the best net yield with 1-year and 5-year projections.
tier: free
inputs: accounts, deposit_amount
---

# High Yield Savings Comparator

## Description
Compares multiple savings accounts by incorporating APY, minimum balances, and monthly fees to surface the best net yield with 1-year and 5-year projections.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `accounts` | `array` | Yes | List of account configs with name, apy, min_balance, monthly_fee, and fee_waiver_balance. |
| `deposit_amount` | `number` | Yes | Dollar amount to deposit, must be non-negative. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "high_yield_savings_comparator",
  "arguments": {
    "accounts": [],
    "deposit_amount": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "high_yield_savings_comparator"`.
