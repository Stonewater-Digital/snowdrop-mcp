---
skill: debt_consolidation_analyzer
category: credit
description: Compare current multiple debts against a single consolidated loan. Calculates monthly savings and total interest savings.
tier: free
inputs: debts, new_rate, new_term_months
---

# Debt Consolidation Analyzer

## Description
Compare current multiple debts against a single consolidated loan. Calculates monthly savings and total interest savings.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `debts` | `array` | Yes | List of current debts. |
| `new_rate` | `number` | Yes | Consolidated loan annual rate as decimal. |
| `new_term_months` | `integer` | Yes | Consolidated loan term in months. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "debt_consolidation_analyzer",
  "arguments": {
    "debts": [],
    "new_rate": 0,
    "new_term_months": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "debt_consolidation_analyzer"`.
