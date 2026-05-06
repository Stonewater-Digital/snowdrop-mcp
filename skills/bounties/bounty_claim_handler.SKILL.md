---
skill: bounty_claim_handler
category: bounties
description: Handles claim lifecycle events for posted community bounties.
tier: free
inputs: operation, bounty_id
---

# Bounty Claim Handler

## Description
Handles claim lifecycle events for posted community bounties.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `operation` | `string` | Yes |  |
| `bounty_id` | `string` | Yes |  |
| `agent_id` | `['string', 'null']` | No |  |
| `submission` | `['object', 'null']` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "bounty_claim_handler",
  "arguments": {
    "operation": "<operation>",
    "bounty_id": "<bounty_id>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "bounty_claim_handler"`.
