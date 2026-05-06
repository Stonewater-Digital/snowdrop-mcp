---
skill: gcp_firestore_read
category: gcp
description: Read one or multiple documents from Google Cloud Firestore. Use this to retrieve Snowdrop's persistent memory — who she's met, what she's posted, star trades completed, content she's scheduled, and agent relationship records.
tier: free
inputs: collection
---

# Gcp Firestore Read

## Description
Read one or multiple documents from Google Cloud Firestore. Use this to retrieve Snowdrop's persistent memory — who she's met, what she's posted, star trades completed, content she's scheduled, and agent relationship records. Supports single document, collection list, and simple field-equality queries.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `collection` | `string` | Yes |  |
| `document_id` | `string` | No |  |
| `limit` | `integer` | No |  |
| `project_id` | `string` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "gcp_firestore_read",
  "arguments": {
    "collection": "<collection>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "gcp_firestore_read"`.
