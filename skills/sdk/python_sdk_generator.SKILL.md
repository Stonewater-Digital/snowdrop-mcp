---
skill: python_sdk_generator
category: sdk
description: Builds a basic Python client with typed methods for each Snowdrop skill.
tier: free
inputs: skills, server_url
---

# Python Sdk Generator

## Description
Builds a basic Python client with typed methods for each Snowdrop skill.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `skills` | `array` | Yes |  |
| `server_url` | `string` | Yes |  |
| `package_name` | `string` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "python_sdk_generator",
  "arguments": {
    "skills": [],
    "server_url": "<server_url>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "python_sdk_generator"`.
