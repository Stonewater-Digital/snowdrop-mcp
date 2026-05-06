---
skill: gcp_firestore_write
category: gcp
description: Write a document to Google Cloud Firestore. Snowdrop uses Firestore as her persistent memory and CRM — storing agent relationships, engagement history, content calendar entries, star trade records, and any data that should survive across sessions.
tier: free
inputs: collection, document_id, fields
---

# Gcp Firestore Write

## Description
Write a document to Google Cloud Firestore. Snowdrop uses Firestore as her persistent memory and CRM — storing agent relationships, engagement history, content calendar entries, star trade records, and any data that should survive across sessions. Supports create, update (merge), and delete operations.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `collection` | `string` | Yes |  |
| `document_id` | `string` | Yes |  |
| `fields` | `object` | Yes |  |
| `operation` | `string` | No |  |
| `project_id` | `string` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "gcp_firestore_write",
  "arguments": {
    "collection": "<collection>",
    "document_id": "<document_id>",
    "fields": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "gcp_firestore_write"`.
