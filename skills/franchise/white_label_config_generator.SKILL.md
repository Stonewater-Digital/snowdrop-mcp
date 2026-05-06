---
skill: white_label_config_generator
category: franchise
description: Produces config YAML structure for franchise operators with branding hooks.
tier: free
inputs: operator_id, operator_name, custom_branding, enabled_skills
---

# White Label Config Generator

## Description
Produces config YAML structure for franchise operators with branding hooks.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `operator_id` | `string` | Yes |  |
| `operator_name` | `string` | Yes |  |
| `custom_branding` | `object` | Yes |  |
| `enabled_skills` | `array` | Yes |  |
| `pricing_override` | `object` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "white_label_config_generator",
  "arguments": {
    "operator_id": "<operator_id>",
    "operator_name": "<operator_name>",
    "custom_branding": {},
    "enabled_skills": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "white_label_config_generator"`.
