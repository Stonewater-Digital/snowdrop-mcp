---
skill: firebase_ml_get_model
category: root
description: Get details of a specific Firebase ML model including its download URI for TFLite deployment.
tier: free
inputs: model_id
---

# Firebase Ml Get Model

## Description
Get details of a specific Firebase ML model including its download URI for TFLite deployment.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `model_id` | `string` | Yes |  |
| `project_id` | `string` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "firebase_ml_get_model",
  "arguments": {
    "model_id": "<model_id>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "firebase_ml_get_model"`.
