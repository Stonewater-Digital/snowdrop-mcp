---
skill: insurance_coverage_tracker
category: insurance
description: Summarizes insurance coverages, gaps, and renewal windows.
tier: free
inputs: policies, current_date
---

# Insurance Coverage Tracker

## Description
Summarizes insurance coverages, gaps, and renewal windows.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `policies` | `array` | Yes |  |
| `current_date` | `string` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "insurance_coverage_tracker",
  "arguments": {
    "policies": [],
    "current_date": "<current_date>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "insurance_coverage_tracker"`.
