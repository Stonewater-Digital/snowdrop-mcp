---
skill: community_impact_attributor
category: crowd_economics
description: Splits revenue, usage, and profit between community and internal skills.
tier: free
inputs: skills_with_revenue
---

# Community Impact Attributor

## Description
Splits revenue, usage, and profit between community and internal skills.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `skills_with_revenue` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "community_impact_attributor",
  "arguments": {
    "skills_with_revenue": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "community_impact_attributor"`.
