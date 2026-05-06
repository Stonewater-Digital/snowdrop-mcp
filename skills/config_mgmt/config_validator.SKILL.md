---
skill: config_validator
category: config_mgmt
description: Ensures config.yaml content meets Snowdrop schema expectations.
tier: free
inputs: config
---

# Config Validator

## Description
Ensures config.yaml content meets Snowdrop schema expectations.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `config` | `object` | Yes |  |
| `required_sections` | `array` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "config_validator",
  "arguments": {
    "config": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "config_validator"`.
