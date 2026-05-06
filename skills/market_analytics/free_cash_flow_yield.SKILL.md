---
skill: free_cash_flow_yield
category: market_analytics
description: Derives free cash flow yield and compares against earnings/dividend yields when available.
tier: free
inputs: operating_cash_flow, capex, stock_price, shares_outstanding
---

# Free Cash Flow Yield

## Description
Derives free cash flow yield and compares against earnings/dividend yields when available.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `operating_cash_flow` | `number` | Yes | Operating cash flow (annual). |
| `capex` | `number` | Yes | Capital expenditures (annual). |
| `stock_price` | `number` | Yes | Current share price. |
| `shares_outstanding` | `number` | Yes | Shares outstanding. |
| `dividend_yield` | `number` | No | Optional dividend yield. |
| `eps` | `number` | No | Optional EPS for earnings yield comparison. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "free_cash_flow_yield",
  "arguments": {
    "operating_cash_flow": 0,
    "capex": 0,
    "stock_price": 0,
    "shares_outstanding": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "free_cash_flow_yield"`.
