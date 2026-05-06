---
skill: agent_to_agent_negotiation
category: social
description: Executes one round of a structured bot-to-bot price negotiation, generating a counter-offer or accept/walk-away recommendation within a 5-round protocol.
tier: free
inputs: our_offer, their_ask, our_limits
---

# Agent To Agent Negotiation

## Description
Executes one round of a structured bot-to-bot price negotiation, generating a counter-offer or accept/walk-away recommendation within a 5-round protocol.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `our_offer` | `object` | Yes | Dict with service (str), price (float), terms (str). |
| `their_ask` | `object` | Yes | Dict with service (str), price (float), terms (str). |
| `our_limits` | `object` | Yes | Dict with min_price (float) and max_concessions (int, max rounds we'll negotiate). |
| `round_number` | `integer` | No | Current negotiation round (1-indexed). Defaults to 1. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "agent_to_agent_negotiation",
  "arguments": {
    "our_offer": {},
    "their_ask": {},
    "our_limits": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "agent_to_agent_negotiation"`.
