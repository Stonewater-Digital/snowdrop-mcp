---
skill: dupont_analysis
category: public_finance
description: Returns 3-stage and 5-stage DuPont ROE decomposition.
tier: free
inputs: net_income, revenue, total_assets, total_equity, ebit, pretax_income, interest_expense
---

# Dupont Analysis

## Description
Returns 3-stage and 5-stage DuPont ROE decomposition.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `net_income` | `number` | Yes |  |
| `revenue` | `number` | Yes |  |
| `total_assets` | `number` | Yes |  |
| `total_equity` | `number` | Yes |  |
| `ebit` | `number` | Yes |  |
| `pretax_income` | `number` | Yes |  |
| `interest_expense` | `number` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "dupont_analysis",
  "arguments": {
    "net_income": 0,
    "revenue": 0,
    "total_assets": 0,
    "total_equity": 0,
    "ebit": 0,
    "pretax_income": 0,
    "interest_expense": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "dupont_analysis"`.
