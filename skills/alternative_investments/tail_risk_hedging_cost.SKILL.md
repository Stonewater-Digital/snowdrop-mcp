---
skill: tail_risk_hedging_cost
category: alternative_investments
description: Aggregates put option strikes/premiums to estimate hedge cost, drawdown coverage, and breakeven levels. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: portfolio_value, put_strikes, put_premiums, target_protection_level
---

# Tail Risk Hedging Cost

## Description
Aggregates put option strikes and premiums across a hedging ladder to estimate total hedge cost, drawdown coverage ratio, and breakeven portfolio levels. Used for systematic tail risk program design and cost-benefit analysis. Premium skill — subscribe at https://snowdrop.ai.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `portfolio_value` | `number` | Yes | Current portfolio market value being hedged (dollars). |
| `put_strikes` | `array` | Yes | List of put option strike prices as portfolio level fractions (e.g. [0.95, 0.90, 0.85]). |
| `put_premiums` | `array` | Yes | List of option premiums as a fraction of notional per strike (same length as put_strikes). |
| `target_protection_level` | `number` | Yes | Target drawdown protection floor as a decimal (e.g. 0.80 for 80% of portfolio). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "tail_risk_hedging_cost",
  "arguments": {
    "portfolio_value": 100000000,
    "put_strikes": [0.95, 0.90, 0.85],
    "put_premiums": [0.018, 0.010, 0.006],
    "target_protection_level": 0.85
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "tail_risk_hedging_cost"`.
