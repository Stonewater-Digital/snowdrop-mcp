---
skill: railway_deploy_status
category: technical
description: Builds Railway GraphQL queries and parses deployment states when provided.
tier: free
inputs: project_id, service_id
---

# Railway Deploy Status

## Description
Builds Railway GraphQL queries and parses deployment states when provided.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `project_id` | `string` | Yes |  |
| `service_id` | `string` | Yes |  |
| `environment_id` | `string` | No |  |
| `api_response` | `object` | No | Optional GraphQL response to parse for status. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "railway_deploy_status",
  "arguments": {
    "project_id": "<project_id>",
    "service_id": "<service_id>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "railway_deploy_status"`.
