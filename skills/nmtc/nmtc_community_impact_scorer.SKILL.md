---
skill: nmtc_community_impact_scorer
category: nmtc
description: Scores NMTC projects across jobs, needs, and community benefits.
tier: free
inputs: project, census_tract
---

# Nmtc Community Impact Scorer

## Description
Scores NMTC projects across jobs, needs, and community benefits.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `project` | `object` | Yes |  |
| `census_tract` | `object` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "nmtc_community_impact_scorer",
  "arguments": {
    "project": {},
    "census_tract": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "nmtc_community_impact_scorer"`.
