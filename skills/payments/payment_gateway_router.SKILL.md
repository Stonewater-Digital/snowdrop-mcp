---
skill: payment_gateway_router
category: payments
description: Determines which verification skill should process a payment receipt.
tier: free
inputs: currency, transaction_ref, expected_amount, payer_agent_id
---

# Payment Gateway Router

## Description
Determines which verification skill should process a payment receipt.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `currency` | `string` | Yes |  |
| `transaction_ref` | `string` | Yes |  |
| `expected_amount` | `number` | Yes |  |
| `payer_agent_id` | `string` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "payment_gateway_router",
  "arguments": {
    "currency": "<currency>",
    "transaction_ref": "<transaction_ref>",
    "expected_amount": 0,
    "payer_agent_id": "<payer_agent_id>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "payment_gateway_router"`.
