---
skill: fund_of_funds_optimizer
category: alternative_investments
description: Uses scenario analysis with CVaR targeting to produce FoF weights under allocation caps. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: fund_return_scenarios, target_return, max_allocation
---

# Fund of Funds Optimizer

## Description
Uses scenario analysis with CVaR targeting to produce fund-of-funds weights under per-fund allocation caps. Optimizes the portfolio for risk-adjusted return across supplied return scenarios. Premium skill — subscribe at https://snowdrop.ai.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `fund_return_scenarios` | `array` | Yes | 2D list of return scenarios: each inner list is one fund's returns across scenarios. |
| `target_return` | `number` | Yes | Target portfolio return as a decimal (e.g. 0.12 for 12%). |
| `max_allocation` | `number` | Yes | Maximum allocation to any single fund as a decimal (e.g. 0.30 for 30%). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "fund_of_funds_optimizer",
  "arguments": {
    "fund_return_scenarios": [
      [0.10, 0.12, 0.08, 0.15],
      [0.07, 0.09, 0.11, 0.06],
      [0.14, 0.11, 0.13, 0.10]
    ],
    "target_return": 0.10,
    "max_allocation": 0.40
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "fund_of_funds_optimizer"`.
