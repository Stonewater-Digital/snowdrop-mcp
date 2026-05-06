---
skill: token_standard_control_person_limit_monitor
category: crypto_rwa
description: Tracks beneficial ownership percentages to enforce control-person caps.
tier: free
inputs: payload
---

# Token Standard Control Person Limit Monitor

## Description
Tracks beneficial ownership percentages to enforce control-person caps.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `payload` | `any` | Yes |  |
| `context` | `any` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "token_standard_control_person_limit_monitor",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "token_standard_control_person_limit_monitor"`.
