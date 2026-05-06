---
skill: firebase_remote_config_get
category: root
description: Get the current Firebase Remote Config template, including all parameters, parameter groups, and conditions.
tier: free
inputs: none
---

# Firebase Remote Config Get

## Description
Get the current Firebase Remote Config template, including all parameters, parameter groups, and conditions.

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
  "tool": "firebase_remote_config_get",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "firebase_remote_config_get"`.
