---
skill: cloud_run_deploy
category: root
description: Deploy, inspect, list, or delete Google Cloud Run services. Uses Cloud Run Admin API v2 with explicit service account credentials only — no gcloud CLI, no Application Default Credentials.
tier: free
inputs: action
---

# Cloud Run Deploy

## Description
Deploy, inspect, list, or delete Google Cloud Run services. Uses Cloud Run Admin API v2 with explicit service account credentials only — no gcloud CLI, no Application Default Credentials.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `action` | `string` | Yes | Operation to perform. |
| `service_name` | `string` | No | Cloud Run service name. |
| `image_url` | `string` | No | Docker image URI (required for deploy). |
| `region` | `string` | No |  |
| `project_id` | `string` | No | GCP project ID (falls back to GOOGLE_PROJECT_ID env). |
| `env_vars` | `object` | No | Key/value environment variables for the service. |
| `port` | `integer` | No |  |
| `memory` | `string` | No |  |
| `cpu` | `string` | No |  |
| `min_instances` | `integer` | No |  |
| `max_instances` | `integer` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "cloud_run_deploy",
  "arguments": {
    "action": "<action>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "cloud_run_deploy"`.
