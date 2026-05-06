---
skill: env_var_auditor
category: config_mgmt
description: Finds missing, empty, and extra environment variables relative to .env.template.
tier: free
inputs: template_vars, set_vars
---

# Env Var Auditor

## Description
Finds missing, empty, and extra environment variables relative to .env.template.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `template_vars` | `array` | Yes |  |
| `set_vars` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "env_var_auditor",
  "arguments": {
    "template_vars": [],
    "set_vars": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "env_var_auditor"`.
