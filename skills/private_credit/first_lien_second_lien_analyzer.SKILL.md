---
skill: first_lien_second_lien_analyzer
category: private_credit
description: Allocates recovery value between first-lien and second-lien creditors.
tier: free
inputs: enterprise_value, senior_debt, junior_debt
---

# First Lien Second Lien Analyzer

## Description
Allocates recovery value between first-lien and second-lien creditors.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `enterprise_value` | `number` | Yes |  |
| `senior_debt` | `number` | Yes |  |
| `junior_debt` | `number` | Yes |  |
| `recovery_pct` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "first_lien_second_lien_analyzer",
  "arguments": {
    "enterprise_value": 0,
    "senior_debt": 0,
    "junior_debt": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "first_lien_second_lien_analyzer"`.
