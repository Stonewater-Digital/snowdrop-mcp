---
skill: portfolio_rebalancing_calculator
category: personal_finance
description: Compares current holdings with target allocations to produce trade instructions, drift metrics, and tax lot reminders for selling positions.
tier: free
inputs: current_holdings, target_allocation
---

# Portfolio Rebalancing Calculator

## Description
Compares current holdings with target allocations to produce trade instructions, drift metrics, and tax lot reminders for selling positions.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `current_holdings` | `array` | Yes | List of holdings with ticker and value fields. |
| `target_allocation` | `array` | Yes | Target weights expressed as percentage decimals per ticker. |
| `new_contribution` | `number` | No | Optional fresh cash to deploy before sales are triggered. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "portfolio_rebalancing_calculator",
  "arguments": {
    "current_holdings": [],
    "target_allocation": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "portfolio_rebalancing_calculator"`.
