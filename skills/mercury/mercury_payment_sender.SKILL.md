---
skill: mercury_payment_sender
category: mercury
description: Constructs ACH/wire payloads for Mercury but leaves them pending Thunder approval.
tier: free
inputs: origin_account_id, amount, beneficiary
---

# Mercury Payment Sender

## Description
Constructs ACH/wire payloads for Mercury but leaves them pending Thunder approval.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `origin_account_id` | `string` | Yes |  |
| `amount` | `number` | Yes |  |
| `currency` | `string` | No |  |
| `memo` | `string` | No |  |
| `beneficiary` | `object` | Yes | Beneficiary wiring instructions. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "mercury_payment_sender",
  "arguments": {
    "origin_account_id": "<origin_account_id>",
    "amount": 0,
    "beneficiary": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "mercury_payment_sender"`.
