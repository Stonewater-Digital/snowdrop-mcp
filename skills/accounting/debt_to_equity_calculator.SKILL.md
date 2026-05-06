---
skill: debt_to_equity_calculator
category: accounting
description: Calculates the debt-to-equity ratio, measuring how much debt a company uses relative to shareholder equity.
tier: free
inputs: total_debt, total_equity
---

# Debt To Equity Calculator

## Description
Calculates the debt-to-equity ratio, measuring how much debt a company uses relative to shareholder equity.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `total_debt` | `number` | Yes | Total debt (short-term + long-term). |
| `total_equity` | `number` | Yes | Total shareholders equity. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "debt_to_equity_calculator",
  "arguments": {
    "total_debt": 0,
    "total_equity": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "debt_to_equity_calculator"`.
