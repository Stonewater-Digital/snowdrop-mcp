---
skill: working_capital_analyzer
category: small_business
description: Computes days sales outstanding, inventory days, days payable outstanding, cash conversion cycle, and highlights improvement opportunities.
tier: free
inputs: accounts_receivable, inventory, accounts_payable, daily_revenue, daily_cogs
---

# Working Capital Analyzer

## Description
Computes days sales outstanding, inventory days, days payable outstanding, cash conversion cycle, and highlights improvement opportunities.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `accounts_receivable` | `number` | Yes | Current accounts receivable balance. |
| `inventory` | `number` | Yes | Inventory balance. |
| `accounts_payable` | `number` | Yes | Accounts payable balance. |
| `daily_revenue` | `number` | Yes | Average daily revenue. |
| `daily_cogs` | `number` | Yes | Average daily cost of goods sold. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "working_capital_analyzer",
  "arguments": {
    "accounts_receivable": 0,
    "inventory": 0,
    "accounts_payable": 0,
    "daily_revenue": 0,
    "daily_cogs": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "working_capital_analyzer"`.
