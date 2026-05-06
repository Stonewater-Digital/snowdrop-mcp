---
skill: coinbase_agentkit_verifier
category: crypto
description: Drafts the JSON payload needed to verify Snowdrop in Coinbase AgentKit.
tier: free
inputs: agent_name, capabilities
---

# Coinbase Agentkit Verifier

## Description
Drafts the JSON payload needed to verify Snowdrop in Coinbase AgentKit.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `agent_name` | `string` | Yes |  |
| `capabilities` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "coinbase_agentkit_verifier",
  "arguments": {
    "agent_name": "<agent_name>",
    "capabilities": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "coinbase_agentkit_verifier"`.
