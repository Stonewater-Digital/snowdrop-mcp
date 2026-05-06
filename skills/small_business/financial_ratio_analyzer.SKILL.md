---
skill: financial_ratio_analyzer
category: small_business
description: Calculates common liquidity, leverage, and profitability ratios using provided balance sheet and income statement figures.
tier: free
inputs: balance_sheet, income_statement
---

# Financial Ratio Analyzer

## Description
Calculates common liquidity, leverage, and profitability ratios using provided balance sheet and income statement figures.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `balance_sheet` | `object` | Yes | Dictionary containing current_assets, inventory, current_liabilities, total_liabilities, shareholders_equity, total_assets. |
| `income_statement` | `object` | Yes | Dictionary containing revenue, gross_profit, net_income, cogs. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "financial_ratio_analyzer",
  "arguments": {
    "balance_sheet": {},
    "income_statement": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "financial_ratio_analyzer"`.
