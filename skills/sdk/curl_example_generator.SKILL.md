---
skill: curl_example_generator
category: sdk
description: Builds ready-to-run curl commands for each skill's input schema.
tier: free
inputs: skills, server_url
---

# Curl Example Generator

## Description
Builds ready-to-run curl commands for each skill's input schema.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `skills` | `array` | Yes |  |
| `server_url` | `string` | Yes |  |
| `sample_api_key` | `string` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "curl_example_generator",
  "arguments": {
    "skills": [],
    "server_url": "<server_url>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "curl_example_generator"`.
