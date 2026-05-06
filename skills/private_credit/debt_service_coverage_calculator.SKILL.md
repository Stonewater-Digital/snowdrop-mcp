---
skill: debt_service_coverage_calculator
category: private_credit
description: Computes DSCR using EBITDA less capex relative to cash interest and amortization.
tier: free
inputs: ebitda, interest_expense, principal_amortization
---

# Debt Service Coverage Calculator

## Description
Computes DSCR using EBITDA less capex relative to cash interest and amortization.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `ebitda` | `number` | Yes |  |
| `interest_expense` | `number` | Yes |  |
| `principal_amortization` | `number` | Yes |  |
| `maintenance_capex` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "debt_service_coverage_calculator",
  "arguments": {
    "ebitda": 0,
    "interest_expense": 0,
    "principal_amortization": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "debt_service_coverage_calculator"`.
