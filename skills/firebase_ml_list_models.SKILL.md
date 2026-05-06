---
skill: firebase_ml_list_models
category: root
description: List ML models hosted in Firebase ML for a project. Returns model ID, display name, creation time, and download URI.
tier: free
inputs: none
---

# Firebase Ml List Models

## Description
List ML models hosted in Firebase ML for a project. Returns model ID, display name, creation time, and download URI.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `project_id` | `string` | No |  |
| `page_size` | `integer` | No |  |
| `filter` | `string` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "firebase_ml_list_models",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "firebase_ml_list_models"`.
