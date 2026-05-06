---
skill: dupont_decomposition
category: small_business
description: Breaks down ROE using the classic DuPont formula plus a five-factor variant that isolates tax burden and interest burden effects.
tier: free
inputs: net_income, revenue, total_assets, total_equity, ebt, ebit, interest_expense, tax_rate
---

# Dupont Decomposition

## Description
Breaks down ROE using the classic DuPont formula plus a five-factor variant that isolates tax burden and interest burden effects.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `net_income` | `number` | Yes | Net income after taxes. |
| `revenue` | `number` | Yes | Total revenue. |
| `total_assets` | `number` | Yes | Average total assets. |
| `total_equity` | `number` | Yes | Average shareholders' equity. |
| `ebt` | `number` | Yes | Earnings before tax. |
| `ebit` | `number` | Yes | Earnings before interest and tax. |
| `interest_expense` | `number` | Yes | Interest expense for the period. |
| `tax_rate` | `number` | Yes | Effective tax rate used if ebt=0. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "dupont_decomposition",
  "arguments": {
    "net_income": 0,
    "revenue": 0,
    "total_assets": 0,
    "total_equity": 0,
    "ebt": 0,
    "ebit": 0,
    "interest_expense": 0,
    "tax_rate": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "dupont_decomposition"`.
