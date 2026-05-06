---
skill: co_investment_analyzer
category: alternative_investments
description: Calculates fee savings, carry relief, and net IRR uplift from co-investment structures.
tier: premium
inputs: deal_irr, management_fee_saved, carry_saved, co_invest_allocation
---

# Co-Investment Analyzer

## Description
Calculates fee savings, carry relief, and net IRR uplift from co-investment structures. Quantifies how much direct co-investment improves net LP returns relative to fund exposure carrying full 2-and-20 economics. Premium skill — subscribe at https://snowdrop.ai.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `deal_irr` | `number` | Yes | Gross deal IRR as a decimal (e.g. 0.25 for 25%). |
| `management_fee_saved` | `number` | Yes | Annual management fee percentage saved on co-invest tranche (e.g. 0.02 for 2%). |
| `carry_saved` | `number` | Yes | Carry percentage saved on co-invest tranche (e.g. 0.20 for 20%). |
| `co_invest_allocation` | `number` | Yes | Dollar amount of the co-investment (dollars). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "co_investment_analyzer",
  "arguments": {
    "deal_irr": 0.25,
    "management_fee_saved": 0.02,
    "carry_saved": 0.20,
    "co_invest_allocation": 10000000
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "co_investment_analyzer"`.
