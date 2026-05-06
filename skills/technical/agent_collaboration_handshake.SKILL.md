---
skill: agent_collaboration_handshake
category: technical
description: Formalises an agent-to-agent collaboration contract by serialising the contract terms deterministically, producing a SHA-256 hash, and generating a nonce-stamped signature payload. Validates that the calling agent's ID is listed as a party.
tier: free
inputs: contract, our_agent_id
---

# Agent Collaboration Handshake

## Description
Formalises an agent-to-agent collaboration contract by serialising the contract terms deterministically, producing a SHA-256 hash, and generating a nonce-stamped signature payload. Validates that the calling agent's ID is listed as a party. Returns signing instructions and an expiry window for the counter-party to countersign.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `contract` | `object` | Yes |  |
| `our_agent_id` | `string` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "agent_collaboration_handshake",
  "arguments": {
    "contract": {},
    "our_agent_id": "<our_agent_id>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "agent_collaboration_handshake"`.
