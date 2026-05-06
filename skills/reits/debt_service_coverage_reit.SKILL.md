---
skill: debt_service_coverage_reit
category: reits
description: Computes DSCR using NOI less recurring capex versus debt service.
tier: free
inputs: net_operating_income, interest_expense, principal_amortization
---

# Debt Service Coverage Reit

## Description
Computes DSCR using NOI less recurring capex versus debt service.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `net_operating_income` | `number` | Yes |  |
| `recurring_capex` | `number` | No |  |
| `interest_expense` | `number` | Yes |  |
| `principal_amortization` | `number` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "debt_service_coverage_reit",
  "arguments": {
    "net_operating_income": 0,
    "interest_expense": 0,
    "principal_amortization": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "debt_service_coverage_reit"`.
