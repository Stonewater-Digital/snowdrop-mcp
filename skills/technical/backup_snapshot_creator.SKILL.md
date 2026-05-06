---
skill: backup_snapshot_creator
category: technical
description: Compiles file manifests for Snowdrop backups (no writes performed).
tier: free
inputs: snapshot_type
---

# Backup Snapshot Creator

## Description
Compiles file manifests for Snowdrop backups (no writes performed).

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `snapshot_type` | `string` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "backup_snapshot_creator",
  "arguments": {
    "snapshot_type": "<snapshot_type>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "backup_snapshot_creator"`.
