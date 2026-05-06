---
skill: firebase_firestore_write
category: root
description: Set, update, or delete a Firestore document. Use operation='set' to replace, 'update' to merge fields, 'delete' to remove document.
tier: free
inputs: none
---

# Firebase Firestore Write

## Description
Set, update, or delete a Firestore document. Use operation='set' to replace, 'update' to merge fields, 'delete' to remove document.

## Parameters
_No parameters defined._

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "firebase_firestore_write",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "firebase_firestore_write"`.
