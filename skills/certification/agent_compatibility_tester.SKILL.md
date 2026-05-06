---
skill: agent_compatibility_tester
category: certification
description: Runs handshake, discovery, and error-handling tests for third-party agents.
tier: free
inputs: agent_id, test_suite, agent_capabilities
---

# Agent Compatibility Tester

## Description
Runs handshake, discovery, and error-handling tests for third-party agents.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `agent_id` | `string` | Yes |  |
| `test_suite` | `string` | Yes |  |
| `agent_capabilities` | `object` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "agent_compatibility_tester",
  "arguments": {
    "agent_id": "<agent_id>",
    "test_suite": "<test_suite>",
    "agent_capabilities": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "agent_compatibility_tester"`.
