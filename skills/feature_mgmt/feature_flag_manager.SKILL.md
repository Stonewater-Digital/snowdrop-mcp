---
skill: feature_flag_manager
category: feature_mgmt
description: Gets, sets, lists, or evaluates feature flags stored in config/feature_flags.json.
tier: free
inputs: operation
---

# Feature Flag Manager

## Description
Gets, sets, lists, or evaluates feature flags stored in config/feature_flags.json.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `operation` | `string` | Yes |  |
| `flag_name` | `string` | No |  |
| `value` | `boolean` | No |  |
| `context` | `object` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "feature_flag_manager",
  "arguments": {
    "operation": "<operation>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "feature_flag_manager"`.
