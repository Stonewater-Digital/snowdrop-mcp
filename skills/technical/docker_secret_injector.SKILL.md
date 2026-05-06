---
skill: docker_secret_injector
category: technical
description: Builds op run templates for injecting secrets into containers.
tier: free
inputs: secret_names, container_name
---

# Docker Secret Injector

## Description
Builds op run templates for injecting secrets into containers.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `secret_names` | `array` | Yes |  |
| `container_name` | `string` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "docker_secret_injector",
  "arguments": {
    "secret_names": [],
    "container_name": "<container_name>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "docker_secret_injector"`.
