---
skill: api_key_rotation_logic
category: technical
description: Evaluates API credential ages against their configured maximum lifetime. Returns three categories: expired keys (must rotate now), expiring-soon keys (within 7 days), and a full rotation schedule sorted by urgency.
tier: free
inputs: credentials
---

# Api Key Rotation Logic

## Description
Evaluates API credential ages against their configured maximum lifetime. Returns three categories: expired keys (must rotate now), expiring-soon keys (within 7 days), and a full rotation schedule sorted by urgency. Also reports an overall compliance percentage.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `credentials` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "api_key_rotation_logic",
  "arguments": {
    "credentials": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "api_key_rotation_logic"`.
