---
skill: ton_payment_verifier
category: payments
description: Validates TON transactions for Snowdrop payments without broadcasting funds.
tier: free
inputs: expected_amount, expected_from, transaction_hash, our_wallet
---

# Ton Payment Verifier

## Description
Validates TON transactions for Snowdrop payments without broadcasting funds.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `expected_amount` | `number` | Yes |  |
| `expected_from` | `string` | Yes |  |
| `transaction_hash` | `string` | Yes |  |
| `our_wallet` | `string` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "ton_payment_verifier",
  "arguments": {
    "expected_amount": 0,
    "expected_from": "<expected_from>",
    "transaction_hash": "<transaction_hash>",
    "our_wallet": "<our_wallet>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "ton_payment_verifier"`.
