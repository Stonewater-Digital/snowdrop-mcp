---
skill: trust_score_calculator
category: trust
description: Combines signals such as payments, vouches, and disputes into a trust tier.
tier: free
inputs: agent_id, signals
---

# Trust Score Calculator

## Description
Combines signals such as payments, vouches, and disputes into a trust tier.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `agent_id` | `string` | Yes |  |
| `signals` | `object` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "trust_score_calculator",
  "arguments": {
    "agent_id": "<agent_id>",
    "signals": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "trust_score_calculator"`.
