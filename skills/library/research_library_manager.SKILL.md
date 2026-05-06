---
skill: research_library_manager
category: library
description: Publishes and queries Goodwill research papers for the community.
tier: free
inputs: operation
---

# Research Library Manager

## Description
Publishes and queries Goodwill research papers for the community.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `operation` | `string` | Yes |  |
| `paper` | `['object', 'null']` | No |  |
| `search_query` | `['string', 'null']` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "research_library_manager",
  "arguments": {
    "operation": "<operation>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "research_library_manager"`.
