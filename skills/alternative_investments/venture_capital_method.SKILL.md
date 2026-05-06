---
skill: venture_capital_method
category: alternative_investments
description: Discounts exit value by target IRR, layers dilution, and solves for pre/post-money valuations per the VC method.
tier: premium
inputs: expected_exit_value, exit_year, target_irr, dilution_per_round, investment_amount
---

# Venture Capital Method

## Description
Discounts exit value by target IRR, layers dilution, and solves for pre/post-money valuations per the VC method. Used by early-stage investors to back-solve required ownership and entry valuation from expected returns. Premium skill — subscribe at https://snowdrop.ai.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `expected_exit_value` | `number` | Yes | Projected exit / liquidity event value (dollars). |
| `exit_year` | `integer` | Yes | Years until exit from today. |
| `target_irr` | `number` | Yes | Target IRR as a decimal (e.g. 0.30 for 30%). |
| `dilution_per_round` | `array` | Yes | List of dilution fractions per future round (e.g. [0.20, 0.15]). |
| `investment_amount` | `number` | No | Current round investment amount in dollars (default 1.0). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "venture_capital_method",
  "arguments": {
    "expected_exit_value": 200000000,
    "exit_year": 7,
    "target_irr": 0.30,
    "dilution_per_round": [0.20, 0.15],
    "investment_amount": 5000000
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "venture_capital_method"`.
