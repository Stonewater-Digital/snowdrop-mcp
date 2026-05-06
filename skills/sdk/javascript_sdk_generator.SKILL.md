---
skill: javascript_sdk_generator
category: sdk
description: Builds an ES module client with fetch wrappers and TypeScript types for skills.
tier: free
inputs: skills, server_url
---

# Javascript Sdk Generator

## Description
Builds an ES module client with fetch wrappers and TypeScript types for skills.

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
  "tool": "javascript_sdk_generator",
  "arguments": {
    "skills": [],
    "server_url": "<server_url>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "javascript_sdk_generator"`.
