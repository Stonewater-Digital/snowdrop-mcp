---
skill: tailscale_mesh_healthcheck
category: technical
description: Pulls device metadata from Tailscale and surfaces online/offline state.
tier: free
inputs: none
---

# Tailscale Mesh Healthcheck

## Description
Pulls device metadata from Tailscale and surfaces online/offline state.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tailnet` | `string` | No | Tailnet slug (e.g., example.gmail.com). |
| `devices` | `array` | No | Optional pre-fetched device list. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "tailscale_mesh_healthcheck",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "tailscale_mesh_healthcheck"`.
