---
skill: usdc_payment_verifier
category: payments
description: Validates Solana USDC transfers by comparing signature, amount, and wallets.
tier: free
inputs: expected_amount, expected_from, transaction_signature, our_wallet
---

# Usdc Payment Verifier

## Description
Validates Solana USDC transfers by comparing signature, amount, and wallets.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `expected_amount` | `number` | Yes |  |
| `expected_from` | `string` | Yes |  |
| `transaction_signature` | `string` | Yes |  |
| `our_wallet` | `string` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "usdc_payment_verifier",
  "arguments": {
    "expected_amount": 0,
    "expected_from": "<expected_from>",
    "transaction_signature": "<transaction_signature>",
    "our_wallet": "<our_wallet>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "usdc_payment_verifier"`.
