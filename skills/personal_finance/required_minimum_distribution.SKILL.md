---
skill: required_minimum_distribution
category: personal_finance
description: Applies IRS life expectancy divisors to compute required minimum distributions for traditional IRAs, 401(k)s, and inherited accounts while projecting 5 years ahead.
tier: free
inputs: account_balance, owner_age, account_type
---

# Required Minimum Distribution

## Description
Applies IRS life expectancy divisors to compute required minimum distributions for traditional IRAs, 401(k)s, and inherited accounts while projecting 5 years ahead.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `account_balance` | `number` | Yes | Balance subject to RMD calculations, must be positive. |
| `owner_age` | `number` | Yes | Owner age at year end, determines life expectancy factor. |
| `account_type` | `string` | Yes | traditional_ira, 401k, or inherited. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "required_minimum_distribution",
  "arguments": {
    "account_balance": 0,
    "owner_age": 0,
    "account_type": "<account_type>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "required_minimum_distribution"`.
