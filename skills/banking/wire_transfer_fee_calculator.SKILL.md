---
skill: wire_transfer_fee_calculator
category: banking
description: Calculate total cost of a wire transfer including fees, and express the fee as a percentage of the transfer amount.
tier: free
inputs: amount
---

# Wire Transfer Fee Calculator

## Description
Calculate total cost of a wire transfer including fees, and express the fee as a percentage of the transfer amount.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `amount` | `number` | Yes | Transfer amount in dollars. |
| `domestic` | `boolean` | No | True for domestic wire, False for international (default True). |
| `bank_fee` | `number` | No | Bank wire fee in dollars (default 25.0). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "wire_transfer_fee_calculator",
  "arguments": {
    "amount": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "wire_transfer_fee_calculator"`.
