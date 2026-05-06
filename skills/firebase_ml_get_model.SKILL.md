---
skill: firebase_ml_get_model
category: root
description: Get details of a specific Firebase ML model including its download URI for TFLite deployment.
tier: free
inputs: none
---

# Firebase Ml Get Model

## Description
Get details of a specific Firebase ML model including its download URI for TFLite deployment.

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
  "tool": "firebase_ml_get_model",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "firebase_ml_get_model"`.
