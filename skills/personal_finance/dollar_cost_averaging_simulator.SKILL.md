---
skill: dollar_cost_averaging_simulator
category: personal_finance
description: Runs a dollar-cost averaging simulation against lump sum investing using a price series to determine ending values and identify the winning approach.
tier: free
inputs: total_investment, monthly_amount, historical_prices, period_months
---

# Dollar Cost Averaging Simulator

## Description
Runs a dollar-cost averaging simulation against lump sum investing using a price series to determine ending values and identify the winning approach.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `total_investment` | `number` | Yes | Total capital available if investing lump sum. |
| `monthly_amount` | `number` | Yes | Monthly contribution used for DCA strategy. |
| `historical_prices` | `array` | Yes | List of historical monthly prices ordered chronologically. |
| `period_months` | `number` | Yes | Number of months to simulate (<= len prices). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "dollar_cost_averaging_simulator",
  "arguments": {
    "total_investment": 0,
    "monthly_amount": 0,
    "historical_prices": [],
    "period_months": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "dollar_cost_averaging_simulator"`.
