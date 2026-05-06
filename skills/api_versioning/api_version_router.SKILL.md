---
skill: api_version_router
category: api_versioning
description: Negotiates version routing and flags deprecations for skills.
tier: free
inputs: requested_version, available_versions, skill_name
---

# Api Version Router

## Description
Negotiates version routing and flags deprecations for skills.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `requested_version` | `string` | Yes |  |
| `available_versions` | `array` | Yes |  |
| `skill_name` | `string` | Yes |  |
| `default_version` | `string` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "api_version_router",
  "arguments": {
    "requested_version": "<requested_version>",
    "available_versions": [],
    "skill_name": "<skill_name>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "api_version_router"`.
