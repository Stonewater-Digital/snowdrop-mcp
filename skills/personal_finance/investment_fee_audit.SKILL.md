---
skill: investment_fee_audit
category: personal_finance
description: Tallies management, advisory, and transaction fees across accounts and quantifies the 10-year drag while pointing to expensive providers.
tier: free
inputs: accounts
---

# Investment Fee Audit

## Description
Tallies management, advisory, and transaction fees across accounts and quantifies the 10-year drag while pointing to expensive providers.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `accounts` | `array` | Yes | List of accounts with provider, balance, expense_ratio, advisory_fee, transaction_fees. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "investment_fee_audit",
  "arguments": {
    "accounts": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "investment_fee_audit"`.
