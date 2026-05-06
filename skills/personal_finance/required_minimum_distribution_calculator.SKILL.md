---
skill: required_minimum_distribution_calculator
category: personal_finance
description: Calculate Required Minimum Distribution (RMD) for traditional IRAs and 401(k)s using the IRS Uniform Lifetime Table. Required starting at age 73 (SECURE 2.0 Act).
tier: free
inputs: account_balance, age
---

# Required Minimum Distribution Calculator

## Description
Calculate Required Minimum Distribution (RMD) for traditional IRAs and 401(k)s using the IRS Uniform Lifetime Table. Required starting at age 73 (SECURE 2.0 Act).

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `account_balance` | `number` | Yes | Year-end account balance (prior year December 31). |
| `age` | `integer` | Yes | Account holder's age during the distribution year. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "required_minimum_distribution_calculator",
  "arguments": {
    "account_balance": 0,
    "age": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "required_minimum_distribution_calculator"`.
