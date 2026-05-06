---
skill: credit_card_interest_calculator
category: credit
description: Calculate credit card interest accrued over a billing period using the daily periodic rate method: daily_rate = APR/365, interest = balance * daily_rate * days.
tier: free
inputs: balance, apr
---

# Credit Card Interest Calculator

## Description
Calculate credit card interest accrued over a billing period using the daily periodic rate method: daily_rate = APR/365, interest = balance * daily_rate * days.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `balance` | `number` | Yes | Average daily balance. |
| `apr` | `number` | Yes | Annual Percentage Rate as decimal. |
| `days_in_period` | `integer` | No | Number of days in billing period (default 30). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "credit_card_interest_calculator",
  "arguments": {
    "balance": 0,
    "apr": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "credit_card_interest_calculator"`.
