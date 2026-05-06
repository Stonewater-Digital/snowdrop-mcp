---
skill: reputation_staking
category: trust
description: Locks reputation points against delivery, quality, or fairness claims.
tier: free
inputs: agent_id, claim, stake_amount, claim_type, current_reputation
---

# Reputation Staking

## Description
Locks reputation points against delivery, quality, or fairness claims.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `agent_id` | `string` | Yes |  |
| `claim` | `string` | Yes |  |
| `stake_amount` | `integer` | Yes |  |
| `claim_type` | `string` | Yes |  |
| `current_reputation` | `integer` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "reputation_staking",
  "arguments": {
    "agent_id": "<agent_id>",
    "claim": "<claim>",
    "stake_amount": 0,
    "claim_type": "<claim_type>",
    "current_reputation": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "reputation_staking"`.
