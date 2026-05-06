---
skill: firebase_app_hosting_list_sites
category: root
description: List Firebase App Hosting backends for a project. Returns backend ID, repository URL, deploy status, and live URL.
tier: free
inputs: none
---

# Firebase App Hosting List Sites

## Description
List Firebase App Hosting backends for a project. Returns backend ID, repository URL, deploy status, and live URL.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `project_id` | `string` | No |  |
| `location` | `string` | No |  |
| `page_size` | `integer` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "firebase_app_hosting_list_sites",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "firebase_app_hosting_list_sites"`.
