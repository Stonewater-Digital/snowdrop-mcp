---
skill: accounts_receivable_turnover_calculator
category: accounting
description: Calculates the accounts receivable turnover ratio and average collection period (days sales outstanding).
tier: free
inputs: net_credit_sales, avg_accounts_receivable
---

# Accounts Receivable Turnover Calculator

## Description
Calculates the accounts receivable turnover ratio and average collection period (days sales outstanding).

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `net_credit_sales` | `number` | Yes | Total net credit sales for the period. |
| `avg_accounts_receivable` | `number` | Yes | Average accounts receivable balance for the period. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "accounts_receivable_turnover_calculator",
  "arguments": {
    "net_credit_sales": 0,
    "avg_accounts_receivable": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "accounts_receivable_turnover_calculator"`.
