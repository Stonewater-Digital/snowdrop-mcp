---
skill: trade_break_resolver
category: middle_office
description: Scores trade breaks by aging and category to prioritize remediation.
tier: free
inputs: breaks
---

# Trade Break Resolver

## Description
Scores trade breaks by aging and category to prioritize remediation.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `breaks` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "trade_break_resolver",
  "arguments": {
    "breaks": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "trade_break_resolver"`.
