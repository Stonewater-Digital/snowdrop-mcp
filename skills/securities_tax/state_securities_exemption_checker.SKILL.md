---
skill: state_securities_exemption_checker
category: securities_tax
description: Determines state exemption availability by offering type and investor count.
tier: free
inputs: states, offering_type, investor_count
---

# State Securities Exemption Checker

## Description
Determines state exemption availability by offering type and investor count.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `states` | `array` | Yes |  |
| `offering_type` | `string` | Yes |  |
| `investor_count` | `number` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "state_securities_exemption_checker",
  "arguments": {
    "states": [],
    "offering_type": "<offering_type>",
    "investor_count": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "state_securities_exemption_checker"`.
