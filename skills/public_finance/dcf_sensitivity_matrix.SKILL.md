---
skill: dcf_sensitivity_matrix
category: public_finance
description: Builds a DCF table across WACC and terminal growth assumptions.
tier: free
inputs: free_cash_flows, wacc_range, terminal_growth_range, shares_outstanding, net_debt
---

# Dcf Sensitivity Matrix

## Description
Builds a DCF table across WACC and terminal growth assumptions.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `free_cash_flows` | `array` | Yes |  |
| `wacc_range` | `array` | Yes |  |
| `terminal_growth_range` | `array` | Yes |  |
| `shares_outstanding` | `number` | Yes |  |
| `net_debt` | `number` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "dcf_sensitivity_matrix",
  "arguments": {
    "free_cash_flows": [],
    "wacc_range": [],
    "terminal_growth_range": [],
    "shares_outstanding": 0,
    "net_debt": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "dcf_sensitivity_matrix"`.
