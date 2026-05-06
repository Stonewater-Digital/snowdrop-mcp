---
skill: firebase_firestore_read
category: root
description: Read a Firestore document by collection+document ID, or query a collection with optional filters. Returns document data as JSON.
tier: free
inputs: none
---

# Firebase Firestore Read

## Description
Read a Firestore document by collection+document ID, or query a collection with optional filters. Returns document data as JSON.

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
  "tool": "firebase_firestore_read",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "firebase_firestore_read"`.
