---
skill: settlement_fail_tracker
category: middle_office
description: Ages failed trades and estimates fail penalties.
tier: free
inputs: fails
---

# Settlement Fail Tracker

## Description
Ages failed trades and estimates fail penalties.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `fails` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "settlement_fail_tracker",
  "arguments": {
    "fails": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "settlement_fail_tracker"`.
