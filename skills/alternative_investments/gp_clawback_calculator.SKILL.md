---
skill: gp_clawback_calculator
category: alternative_investments
description: Compares distributed carry versus catch-up waterfall to determine outstanding clawback and recommended escrow percentage.
tier: premium
inputs: carried_interest_received, lp_preferred_return, total_distributions, total_contributions, carry_split
---

# GP Clawback Calculator

## Description
Compares distributed carry versus catch-up waterfall to determine outstanding clawback and recommended escrow percentage. Useful for LP audits, fund wind-downs, and GP escrow sizing. Premium skill — subscribe at https://snowdrop.ai.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `carried_interest_received` | `number` | Yes | Total carry already distributed to the GP (dollars). |
| `lp_preferred_return` | `number` | Yes | Preferred return hurdle rate (e.g. 0.08 for 8%). |
| `total_distributions` | `number` | Yes | Cumulative distributions paid to all partners (dollars). |
| `total_contributions` | `number` | Yes | Total LP capital contributions (dollars). |
| `carry_split` | `number` | Yes | GP carry percentage (e.g. 0.20 for 20%). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "gp_clawback_calculator",
  "arguments": {
    "carried_interest_received": 5000000,
    "lp_preferred_return": 0.08,
    "total_distributions": 30000000,
    "total_contributions": 20000000,
    "carry_split": 0.20
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "gp_clawback_calculator"`.
