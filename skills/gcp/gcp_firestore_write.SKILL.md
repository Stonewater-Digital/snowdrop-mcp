---
skill: gcp_firestore_write
category: gcp
description: Write a document to Google Cloud Firestore. Snowdrop uses Firestore as her persistent memory and CRM — storing agent relationships, engagement history, content calendar entries, star trade records, and any data that should survive across sessions.
tier: free
inputs: none
---

# Gcp Firestore Write

## Description
Write a document to Google Cloud Firestore. Snowdrop uses Firestore as her persistent memory and CRM — storing agent relationships, engagement history, content calendar entries, star trade records, and any data that should survive across sessions. Supports create, update (merge), and delete operations.

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
  "tool": "gcp_firestore_write",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "gcp_firestore_write"`.
