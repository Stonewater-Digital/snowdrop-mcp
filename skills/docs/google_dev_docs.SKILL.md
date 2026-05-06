---
skill: google_dev_docs
category: docs
description: Search Google's official developer documentation via the Developer Knowledge MCP API. Covers Firebase, all Google Cloud services (Cloud Run, BigQuery, Vertex AI, Pub/Sub, Firestore, Secret Manager, etc.), Android, Chrome, Google Maps, TensorFlow, and all Google APIs.
tier: free
inputs: query
---

# Google Dev Docs

## Description
Search Google's official developer documentation via the Developer Knowledge MCP API. Covers Firebase, all Google Cloud services (Cloud Run, BigQuery, Vertex AI, Pub/Sub, Firestore, Secret Manager, etc.), Android, Chrome, Google Maps, TensorFlow, and all Google APIs. Returns authoritative doc snippets re-indexed within 24h of upstream changes. Set fetch_full=True to get the complete page content for the top result. Requires GOOGLE_DEVELOPER_KNOWLEDGE_API_KEY env var.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `query` | `string` | Yes |  |
| `fetch_full` | `boolean` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "google_dev_docs",
  "arguments": {
    "query": "<query>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "google_dev_docs"`.
