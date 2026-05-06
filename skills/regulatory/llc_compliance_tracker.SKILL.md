---
skill: llc_compliance_tracker
category: regulatory
description: Calculates upcoming compliance deadlines for Stonewater Solutions LLC.
tier: free
inputs: formation_date
---

# Llc Compliance Tracker

## Description
Calculates upcoming compliance deadlines for Stonewater Solutions LLC.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `state` | `string` | No |  |
| `formation_date` | `string` | Yes |  |
| `last_annual_report` | `['string', 'null']` | No |  |
| `registered_agent_expiry` | `['string', 'null']` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "llc_compliance_tracker",
  "arguments": {
    "formation_date": "<formation_date>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "llc_compliance_tracker"`.
