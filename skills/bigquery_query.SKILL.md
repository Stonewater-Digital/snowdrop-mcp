---
skill: bigquery_query
category: root
description: Run BigQuery SQL queries and schema operations for financial analytics. Uses BigQuery REST API v2 with explicit SA credentials — no gcloud, no ADC.
tier: free
inputs: action
---

# Bigquery Query

## Description
Run BigQuery SQL queries and schema operations for financial analytics. Uses BigQuery REST API v2 with explicit SA credentials — no gcloud, no ADC. Requires roles/bigquery.jobUser and roles/bigquery.dataViewer.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `action` | `string` | Yes | Operation to perform. |
| `sql` | `string` | No | BigQuery SQL statement (required for query). |
| `project_id` | `string` | No | GCP project ID. |
| `dataset_id` | `string` | No | Dataset ID (required for list_tables). |
| `table_id` | `string` | No | Table ID (required for get_schema). |
| `max_results` | `integer` | No |  |
| `timeout_ms` | `integer` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "bigquery_query",
  "arguments": {
    "action": "<action>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "bigquery_query"`.
