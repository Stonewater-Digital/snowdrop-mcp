---
skill: openapi_spec_generator
category: api_spec
description: Converts Snowdrop skill metadata into an OpenAPI 3.0.3 specification.
tier: free
inputs: skills
---

# Openapi Spec Generator

## Description
Converts Snowdrop skill metadata into an OpenAPI 3.0.3 specification.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `skills` | `array` | Yes |  |
| `server_url` | `string` | No |  |
| `api_version` | `string` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "openapi_spec_generator",
  "arguments": {
    "skills": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "openapi_spec_generator"`.
