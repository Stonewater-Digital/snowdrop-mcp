---
skill: backup_verifier
category: disaster_recovery
description: Checks backup manifests for missing or corrupted files using SHA-256 hashes.
tier: free
inputs: manifest, backup_location
---

# Backup Verifier

## Description
Checks backup manifests for missing or corrupted files using SHA-256 hashes.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `manifest` | `object` | Yes |  |
| `backup_location` | `string` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "backup_verifier",
  "arguments": {
    "manifest": {},
    "backup_location": "<backup_location>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "backup_verifier"`.
