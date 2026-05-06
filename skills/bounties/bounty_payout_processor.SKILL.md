---
skill: bounty_payout_processor
category: bounties
description: Validates and stages payouts for approved bounty winners.
tier: free
inputs: bounty_id, winner_agent_id, approved_amount, currency
---

# Bounty Payout Processor

## Description
Validates and stages payouts for approved bounty winners.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `bounty_id` | `string` | Yes |  |
| `winner_agent_id` | `string` | Yes |  |
| `approved_amount` | `number` | Yes |  |
| `currency` | `string` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "bounty_payout_processor",
  "arguments": {
    "bounty_id": "<bounty_id>",
    "winner_agent_id": "<winner_agent_id>",
    "approved_amount": 0,
    "currency": "<currency>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "bounty_payout_processor"`.
