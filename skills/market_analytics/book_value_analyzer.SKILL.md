---
skill: book_value_analyzer
category: market_analytics
description: Computes book/tangible book per share and related valuation ratios.
tier: free
inputs: total_assets, total_liabilities, intangibles, goodwill, shares_outstanding, stock_price
---

# Book Value Analyzer

## Description
Computes book/tangible book per share and related valuation ratios.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `total_assets` | `number` | Yes | Total assets. |
| `total_liabilities` | `number` | Yes | Total liabilities. |
| `intangibles` | `number` | Yes | Intangible assets. |
| `goodwill` | `number` | Yes | Goodwill on balance sheet. |
| `shares_outstanding` | `number` | Yes | Shares outstanding. |
| `stock_price` | `number` | Yes | Current share price. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "book_value_analyzer",
  "arguments": {
    "total_assets": 0,
    "total_liabilities": 0,
    "intangibles": 0,
    "goodwill": 0,
    "shares_outstanding": 0,
    "stock_price": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "book_value_analyzer"`.
