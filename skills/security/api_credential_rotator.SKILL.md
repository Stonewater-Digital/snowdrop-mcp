---
skill: api_credential_rotator
category: security
description: Generates rotation tasks for API keys/secrets using age vs. policy frequency.
tier: free
inputs: credentials
---

# Api Credential Rotator

## Description
Generates rotation tasks for API keys/secrets using age vs. policy frequency.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `credentials` | `array` | Yes | Credential entries with name, owner, last_rotated_at, rotation_frequency_days, criticality. |
| `notify_thunder` | `boolean` | No | Send Thunder alert when overdue credentials are found. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "api_credential_rotator",
  "arguments": {
    "credentials": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "api_credential_rotator"`.
