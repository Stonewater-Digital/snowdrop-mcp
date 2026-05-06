---
skill: data_transformer
category: etl
description: Applies rename/cast/compute/drop/default transformations to dataset rows sequentially.
tier: free
inputs: data, transformations
---

# Data Transformer

## Description
Applies rename/cast/compute/drop/default transformations to dataset rows sequentially.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `data` | `array` | Yes |  |
| `transformations` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "data_transformer",
  "arguments": {
    "data": [],
    "transformations": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "data_transformer"`.
