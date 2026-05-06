---
skill: what_if_engine
category: simulation
description: Applies scenario overrides to a base business case and projects outcomes.
tier: free
inputs: base_case, scenarios
---

# What If Engine

## Description
Applies scenario overrides to a base business case and projects outcomes.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `base_case` | `object` | Yes |  |
| `scenarios` | `array` | Yes | List of scenario dicts with name and overrides. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "what_if_engine",
  "arguments": {
    "base_case": {},
    "scenarios": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "what_if_engine"`.
