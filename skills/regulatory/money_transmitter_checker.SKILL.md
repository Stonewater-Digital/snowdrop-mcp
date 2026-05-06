---
skill: money_transmitter_checker
category: regulatory
description: Flags actions that might require MTL coverage and provides guidance.
tier: free
inputs: action_type, amount, sender_type, receiver_type, jurisdiction
---

# Money Transmitter Checker

## Description
Flags actions that might require MTL coverage and provides guidance.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `action_type` | `string` | Yes |  |
| `amount` | `number` | Yes |  |
| `sender_type` | `string` | Yes |  |
| `receiver_type` | `string` | Yes |  |
| `jurisdiction` | `string` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "money_transmitter_checker",
  "arguments": {
    "action_type": "<action_type>",
    "amount": 0,
    "sender_type": "<sender_type>",
    "receiver_type": "<receiver_type>",
    "jurisdiction": "<jurisdiction>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "money_transmitter_checker"`.
