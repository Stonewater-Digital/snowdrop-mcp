---
skill: revolving_credit_analyzer
category: credit
description: Analyze revolving credit costs including annual interest cost, utilization ratio, and cost per dollar borrowed.
tier: free
inputs: credit_limit, avg_balance, apr
---

# Revolving Credit Analyzer

## Description
Analyze revolving credit costs including annual interest cost, utilization ratio, and cost per dollar borrowed.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `credit_limit` | `number` | Yes | Total credit limit. |
| `avg_balance` | `number` | Yes | Average revolving balance. |
| `apr` | `number` | Yes | Annual Percentage Rate as decimal. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "revolving_credit_analyzer",
  "arguments": {
    "credit_limit": 0,
    "avg_balance": 0,
    "apr": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "revolving_credit_analyzer"`.
