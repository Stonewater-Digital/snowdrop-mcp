---
skill: secrets_audit_monitor
category: integrations
description: Checks whether required secrets are present in the environment and flags missing/empty variables.
tier: free
inputs: required_secrets
---

# Secrets Audit Monitor

## Description
Checks whether required secrets are present in the environment and flags missing/empty variables.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `required_secrets` | `array` | Yes | Names of env vars that must be set. |
| `env_source` | `object` | No | Optional map of env vars (defaults to os.environ). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "secrets_audit_monitor",
  "arguments": {
    "required_secrets": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "secrets_audit_monitor"`.
