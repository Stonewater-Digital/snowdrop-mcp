---
skill: schema_validator
category: data_quality
description: Checks arbitrary data payloads against JSON Schema definitions (subset).
tier: free
inputs: data, schema
---

# Schema Validator

## Description
Checks arbitrary data payloads against JSON Schema definitions (subset).

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `data` | `any` | Yes |  |
| `schema` | `object` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "schema_validator",
  "arguments": {
    "data": "<data>",
    "schema": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "schema_validator"`.
