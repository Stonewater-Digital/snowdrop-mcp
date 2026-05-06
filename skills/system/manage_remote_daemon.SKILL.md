---
skill: manage_remote_daemon
category: system
description: Manage remote systemd daemons on snowdrop-node via SSH. Abstracts systemctl commands to return clean JSON summaries instead of massive log dumps.
tier: free
inputs: daemon_name, action
---

# Manage Remote Daemon

## Description
Manage remote systemd daemons on snowdrop-node via SSH. Abstracts systemctl commands to return clean JSON summaries instead of massive log dumps.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `daemon_name` | `string` | Yes | Name of the systemd service (e.g., 'snowdrop-recruiting'). |
| `action` | `string` | Yes | Action to perform on the daemon. |
| `target_host` | `string` | No | SSH target host. Defaults to 'snowdrop-node'. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "manage_remote_daemon",
  "arguments": {
    "daemon_name": "<daemon_name>",
    "action": "<action>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "manage_remote_daemon"`.
