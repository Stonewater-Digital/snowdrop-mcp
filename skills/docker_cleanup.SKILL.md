---
skill: docker_cleanup
category: root
description: Clean up Docker images, containers, and volumes on the local machine to prevent disk exhaustion. Supports dry-run mode.
tier: free
inputs: action
---

# Docker Cleanup

## Description
Clean up Docker images, containers, and volumes on the local machine to prevent disk exhaustion. Supports dry-run mode. Schedule weekly via subagent. Always preserve keep_images list (e.g. the live snowdrop-mcp image).

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `action` | `string` | Yes | Cleanup operation to perform. |
| `keep_images` | `array` | No | Image names/tags to preserve. Default: ['snowdrop-mcp:latest'] |
| `dry_run` | `boolean` | No | If true, shows what would be removed without removing anything. |
| `min_age_days` | `integer` | No | Only remove images/containers older than N days. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "docker_cleanup",
  "arguments": {
    "action": "<action>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "docker_cleanup"`.
