---
skill: premium_estimator
category: insurance
description: Provides heuristic premium estimates based on business profile and coverage type.
tier: free
inputs: business_profile, coverage_type
---

# Premium Estimator

## Description
Provides heuristic premium estimates based on business profile and coverage type.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `business_profile` | `object` | Yes |  |
| `coverage_type` | `string` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "premium_estimator",
  "arguments": {
    "business_profile": {},
    "coverage_type": "<coverage_type>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "premium_estimator"`.
