---
skill: artifact_registry_manager
category: root
description: Manage Google Artifact Registry Docker images: list, clean old tags, remove untagged layers. Use after each deployment to keep storage costs low.
tier: free
inputs: action
---

# Artifact Registry Manager

## Description
Manage Google Artifact Registry Docker images: list, clean old tags, remove untagged layers. Use after each deployment to keep storage costs low. Requires roles/artifactregistry.admin on the service account.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `action` | `string` | Yes | Operation to perform. |
| `repository` | `string` | No | Artifact Registry repository name (e.g. 'snowdrop-images'). |
| `location` | `string` | No |  |
| `project_id` | `string` | No | GCP project ID. |
| `keep_latest` | `integer` | No | Number of most-recent tagged versions to keep (for delete_old_tags). |
| `package_name` | `string` | No | Specific image name for list_tags/get_digest. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "artifact_registry_manager",
  "arguments": {
    "action": "<action>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "artifact_registry_manager"`.
