---
skill: portable_alpha_calculator
category: alternative_investments
description: Aggregates returns from alpha and beta sleeves, subtracts hedge cost, and reports contribution along with realized tracking error. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: alpha_returns, beta_returns, hedge_cost
---

# Portable Alpha Calculator

## Description
Aggregates returns from alpha and beta sleeves, subtracts hedge/overlay cost, and reports combined performance attribution along with realized tracking error. Used for evaluating alpha transport strategies. Premium skill — subscribe at https://snowdrop.ai.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `alpha_returns` | `array` | Yes | List of periodic returns from the alpha-generating sleeve (e.g. hedge fund, active strategy). |
| `beta_returns` | `array` | Yes | List of periodic returns from the beta/index overlay sleeve. |
| `hedge_cost` | `number` | Yes | Total annual cost of the derivatives overlay as a decimal (e.g. 0.005 for 50 bps). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "portable_alpha_calculator",
  "arguments": {
    "alpha_returns": [0.012, 0.008, -0.003, 0.015, 0.010],
    "beta_returns": [0.015, -0.005, 0.020, 0.008, 0.012],
    "hedge_cost": 0.005
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "portable_alpha_calculator"`.
