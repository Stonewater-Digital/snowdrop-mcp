---
skill: gcp_secret_manager
category: root
description: Create, read, rotate, list, or delete secrets in Google Cloud Secret Manager. Uses Secret Manager API v1 with explicit service account credentials — no gcloud CLI, no ADC.
tier: free
inputs: action
---

# Gcp Secret Manager

## Description
Create, read, rotate, list, or delete secrets in Google Cloud Secret Manager. Uses Secret Manager API v1 with explicit service account credentials — no gcloud CLI, no ADC. Requires roles/secretmanager.admin on the service account.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `action` | `string` | Yes | Operation to perform. |
| `secret_id` | `string` | No | Secret identifier (required for get/set/delete/rotate). |
| `secret_value` | `string` | No | Plaintext secret value (required for set/rotate). Never logged. |
| `project_id` | `string` | No | GCP project ID (falls back to GOOGLE_PROJECT_ID env). |
| `version` | `string` | No | Secret version to retrieve (for get). Use 'latest' for current. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "gcp_secret_manager",
  "arguments": {
    "action": "<action>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "gcp_secret_manager"`.
