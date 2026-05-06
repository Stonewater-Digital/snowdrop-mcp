---
skill: data_narrator
category: nlg
description: Converts structured finance outputs into tone-aware prose.
tier: free
inputs: data_type, data
---

# Data Narrator

## Description
Converts structured finance outputs into tone-aware prose.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `data_type` | `string` | Yes |  |
| `data` | `object` | Yes |  |
| `tone` | `string` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "data_narrator",
  "arguments": {
    "data_type": "<data_type>",
    "data": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "data_narrator"`.
