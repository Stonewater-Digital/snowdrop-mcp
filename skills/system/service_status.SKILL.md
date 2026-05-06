---
skill: service_status
category: system
description: Check the status of a systemd user service. Returns active state, sub-state, load state, description, and last activation timestamp.
tier: free
inputs: service_name
---

# Service Status

## Description
Check the status of a systemd user service. Returns active state, sub-state, load state, description, and last activation timestamp. Example service names: 'snowdrop-mcp', 'openclaw-gateway'.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `service_name` | `string` | Yes | Systemd user service name, e.g. 'snowdrop-mcp'. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "service_status",
  "arguments": {
    "service_name": "<service_name>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "service_status"`.
