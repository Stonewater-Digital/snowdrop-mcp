---
skill: ton_w5_gasless_transfer
category: technical
description: Build TON W5 wallet gasless transfer payload using battery sponsorship for zero-fee TON movements.
tier: free
inputs: recipient_address, amount_ton
---

# Ton W5 Gasless Transfer

## Description
Build TON W5 wallet gasless transfer payload using battery sponsorship for zero-fee TON movements.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `recipient_address` | `string` | Yes | The TON recipient wallet address (EQ or UQ format). |
| `amount_ton` | `number` | Yes | Amount of TON to transfer (in TON, not nanoton). |
| `memo` | `string` | No | Optional transfer comment/memo. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "ton_w5_gasless_transfer",
  "arguments": {
    "recipient_address": "<recipient_address>",
    "amount_ton": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "ton_w5_gasless_transfer"`.
