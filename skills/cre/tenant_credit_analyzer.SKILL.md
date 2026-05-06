---
skill: tenant_credit_analyzer
category: cre
description: Scores tenant credit strength based on financials and lease metrics.
tier: free
inputs: tenant
---

# Tenant Credit Analyzer

## Description
Scores tenant credit strength based on financials and lease metrics.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tenant` | `object` | Yes |  |
| `property_rent_pct_of_revenue` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "tenant_credit_analyzer",
  "arguments": {
    "tenant": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "tenant_credit_analyzer"`.
