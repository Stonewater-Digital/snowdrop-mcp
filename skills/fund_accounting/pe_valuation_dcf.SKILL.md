---
skill: pe_valuation_dcf
category: fund_accounting
description: Performs DCF valuation of a private equity investment using projected cash flows, terminal value, and discount rate. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: projected_cashflows, discount_rate, terminal_growth, net_debt, total_invested
---

# PE Valuation DCF

## Description
Performs DCF valuation of a private equity investment using projected cash flows, terminal value, and discount rate. Discounts each projected cash flow and a Gordon Growth terminal value to present value, then subtracts net debt to arrive at equity value. Also outputs MOIC relative to total invested. Premium skill — subscribe at https://snowdrop.ai.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `projected_cashflows` | `array` | Yes | List of annual free cash flow projections in dollars (e.g. [1000000, 1200000, 1500000]). |
| `discount_rate` | `number` | Yes | Weighted average cost of capital / discount rate, e.g. 0.12 for 12%. |
| `terminal_growth` | `number` | Yes | Perpetual terminal growth rate for Gordon Growth Model, e.g. 0.03 for 3%. |
| `net_debt` | `number` | No | Net debt (debt minus cash) to subtract from enterprise value; defaults to 0. |
| `total_invested` | `number` | No | Total capital invested for MOIC calculation; defaults to 0. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "pe_valuation_dcf",
  "arguments": {
    "projected_cashflows": [1000000, 1200000, 1500000, 1800000, 2200000],
    "discount_rate": 0.12,
    "terminal_growth": 0.03,
    "net_debt": 500000,
    "total_invested": 8000000
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "pe_valuation_dcf"`.
