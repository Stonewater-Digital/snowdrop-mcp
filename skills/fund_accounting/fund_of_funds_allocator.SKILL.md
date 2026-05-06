---
skill: fund_of_funds_allocator
category: fund_accounting
description: Creates a heuristic allocation maximizing expected return under diversification rules. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: fof_capital, underlying_funds, constraints
---

# Fund Of Funds Allocator

## Description
Creates a heuristic allocation maximizing expected return under diversification rules. (Premium — subscribe at https://snowdrop.ai)

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `fof_capital` | `number` | Yes | Total capital available for allocation in the fund-of-funds in dollars. |
| `underlying_funds` | `array` | Yes | List of underlying fund objects, each with `name`, `strategy`, `expected_net_irr`, `min_commitment`, and `max_commitment`. |
| `constraints` | `object` | Yes | Diversification constraint rules, e.g. `{"max_single_fund_pct": 0.20, "max_strategy_pct": 0.40, "min_funds": 5}`. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "fund_of_funds_allocator",
  "arguments": {
    "fof_capital": 200000000,
    "underlying_funds": [
      {"name": "Buyout Fund A", "strategy": "buyout", "expected_net_irr": 0.18, "min_commitment": 5000000, "max_commitment": 40000000},
      {"name": "Growth Fund B", "strategy": "growth", "expected_net_irr": 0.22, "min_commitment": 5000000, "max_commitment": 30000000},
      {"name": "Venture Fund C", "strategy": "venture", "expected_net_irr": 0.25, "min_commitment": 2000000, "max_commitment": 20000000}
    ],
    "constraints": {"max_single_fund_pct": 0.20, "max_strategy_pct": 0.40, "min_funds": 5}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "fund_of_funds_allocator"`.
