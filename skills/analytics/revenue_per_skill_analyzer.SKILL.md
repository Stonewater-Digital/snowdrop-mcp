---
skill: revenue_per_skill_analyzer
category: analytics
description: Aggregates billing records to highlight top-performing skills and concentration
tier: free
inputs: billing_records, period
---

# Revenue Per Skill Analyzer

## Description
Aggregates billing records to highlight top-performing skills and concentration

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `billing_records` | `array` | Yes |  |
| `period` | `string` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "revenue_per_skill_analyzer",
  "arguments": {
    "billing_records": [],
    "period": "<period>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "revenue_per_skill_analyzer"`.
