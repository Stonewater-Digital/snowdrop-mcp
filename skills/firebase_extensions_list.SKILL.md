---
skill: firebase_extensions_list
category: root
description: List all installed Firebase Extensions in a project. Returns extension instance ID, state, extension reference, and configuration.
tier: free
inputs: none
---

# Firebase Extensions List

## Description
List all installed Firebase Extensions in a project. Returns extension instance ID, state, extension reference, and configuration.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `project_id` | `string` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "firebase_extensions_list",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "firebase_extensions_list"`.
