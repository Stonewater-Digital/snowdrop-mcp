---
skill: notice_filing_requirement_tracker
category: securities_tax
description: Tracks Form D notice filing triggers and deadlines by state.
tier: free
inputs: states, offering_type
---

# Notice Filing Requirement Tracker

## Description
Tracks Form D notice filing triggers and deadlines by state.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `states` | `array` | Yes |  |
| `offering_type` | `string` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "notice_filing_requirement_tracker",
  "arguments": {
    "states": [],
    "offering_type": "<offering_type>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "notice_filing_requirement_tracker"`.
