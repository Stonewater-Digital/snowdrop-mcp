---
skill: firebase_realtime_db_delete
category: root
description: Delete a node from Firebase Realtime Database at the given path.
tier: free
inputs: path
---

# Firebase Realtime Db Delete

## Description
Delete a node from Firebase Realtime Database at the given path.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `path` | `string` | Yes |  |
| `database_url` | `string` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "firebase_realtime_db_delete",
  "arguments": {
    "path": "<path>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "firebase_realtime_db_delete"`.
