---
skill: noi_audit_tool
category: real_estate
description: Validates Net Operating Income (NOI) for a commercial real estate property. Computes NOI from gross revenue and operating expenses, calculates NOI margin, and flags material variance against a prior period if provided.
tier: free
inputs: gross_revenue, operating_expenses
---

# Noi Audit Tool

## Description
Validates Net Operating Income (NOI) for a commercial real estate property. Computes NOI from gross revenue and operating expenses, calculates NOI margin, and flags material variance against a prior period if provided.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `gross_revenue` | `number` | Yes | Total gross revenue for the period (dollars). |
| `operating_expenses` | `number` | Yes | Total operating expenses excluding debt service (dollars). |
| `prior_noi` | `number` | No | NOI from the prior comparable period for variance analysis (optional). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "noi_audit_tool",
  "arguments": {
    "gross_revenue": 0,
    "operating_expenses": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "noi_audit_tool"`.
