---
skill: debt_service_coverage_calculator
category: accounting
description: Calculates the debt service coverage ratio (net operating income / total debt service), used by lenders to assess repayment ability.
tier: free
inputs: net_operating_income, total_debt_service
---

# Debt Service Coverage Calculator

## Description
Calculates the debt service coverage ratio (net operating income / total debt service), used by lenders to assess repayment ability.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `net_operating_income` | `number` | Yes | Net operating income for the period. |
| `total_debt_service` | `number` | Yes | Total debt service (principal + interest payments). |

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
    "net_operating_income": 0,
    "total_debt_service": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "debt_service_coverage_calculator"`.
