---
skill: flyio_deploy_status
category: technical
description: Builds Fly.io API requests and summarizes allocation health.
tier: free
inputs: app_name
---

# Flyio Deploy Status

## Description
Builds Fly.io API requests and summarizes allocation health.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `app_name` | `string` | Yes |  |
| `api_response` | `object` | No | Optional machines API response to parse. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "flyio_deploy_status",
  "arguments": {
    "app_name": "<app_name>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "flyio_deploy_status"`.
