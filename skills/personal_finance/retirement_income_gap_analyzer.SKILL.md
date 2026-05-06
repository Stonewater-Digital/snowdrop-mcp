---
skill: retirement_income_gap_analyzer
category: personal_finance
description: Aggregates guaranteed income sources with planned withdrawals to determine gaps versus target retirement spending and highlight additional savings required.
tier: free
inputs: desired_retirement_income, social_security_estimate, pension_estimate, other_income, portfolio_balance, withdrawal_rate
---

# Retirement Income Gap Analyzer

## Description
Aggregates guaranteed income sources with planned withdrawals to determine gaps versus target retirement spending and highlight additional savings required.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `desired_retirement_income` | `number` | Yes | Annual after-tax lifestyle target in dollars. |
| `social_security_estimate` | `number` | Yes | Annual Social Security benefits, can be zero. |
| `pension_estimate` | `number` | Yes | Annual pension income in dollars. |
| `other_income` | `number` | Yes | Other guaranteed income sources such as annuities. |
| `portfolio_balance` | `number` | Yes | Investable assets available for withdrawals. |
| `withdrawal_rate` | `number` | Yes | Planned sustainable withdrawal rate as decimal. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "retirement_income_gap_analyzer",
  "arguments": {
    "desired_retirement_income": 0,
    "social_security_estimate": 0,
    "pension_estimate": 0,
    "other_income": 0,
    "portfolio_balance": 0,
    "withdrawal_rate": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "retirement_income_gap_analyzer"`.
