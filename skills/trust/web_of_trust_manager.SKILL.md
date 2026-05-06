---
skill: web_of_trust_manager
category: trust
description: Records vouches between agents and exposes trust graph stats.
tier: free
inputs: operation, from_agent
---

# Web Of Trust Manager

## Description
Records vouches between agents and exposes trust graph stats.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `operation` | `string` | Yes |  |
| `from_agent` | `string` | Yes |  |
| `to_agent` | `['string', 'null']` | No |  |
| `vouch_context` | `['string', 'null']` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "web_of_trust_manager",
  "arguments": {
    "operation": "<operation>",
    "from_agent": "<from_agent>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "web_of_trust_manager"`.
