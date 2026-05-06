---
skill: firebase_firestore_write
category: root
description: Set, update, or delete a Firestore document. Use operation='set' to replace, 'update' to merge fields, 'delete' to remove document.
tier: free
inputs: collection, document_id
---

# Firebase Firestore Write

## Description
Set, update, or delete a Firestore document. Use operation='set' to replace, 'update' to merge fields, 'delete' to remove document.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `collection` | `string` | Yes |  |
| `document_id` | `string` | Yes |  |
| `data` | `object` | No |  |
| `operation` | `string` | No |  |
| `merge` | `boolean` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "firebase_firestore_write",
  "arguments": {
    "collection": "<collection>",
    "document_id": "<document_id>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "firebase_firestore_write"`.
