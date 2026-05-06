---
skill: agent_directory_manager
category: agent_directory
description: Registers, updates, searches, and deactivates public agent profiles.
tier: free
inputs: operation
---

# Agent Directory Manager

## Description
Registers, updates, searches, and deactivates public agent profiles.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `operation` | `string` | Yes |  |
| `agent_profile` | `['object', 'null']` | No |  |
| `search_query` | `['string', 'null']` | No |  |
| `filter_capabilities` | `['array', 'null']` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "agent_directory_manager",
  "arguments": {
    "operation": "<operation>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "agent_directory_manager"`.
