---
skill: treasury_sweep_recommender
category: treasury
description: Identifies idle cash available for sweeps and proposes destinations (pending Thunder).
tier: free
inputs: account_balances, monthly_burn
---

# Treasury Sweep Recommender

## Description
Identifies idle cash available for sweeps and proposes destinations (pending Thunder).

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `account_balances` | `object` | Yes | Dictionary mapping account name/ID (string) to current balance in USD (number). |
| `operating_buffer_months` | `integer` | No | Number of months of burn to reserve before sweeping idle cash (default: 3). |
| `monthly_burn` | `number` | Yes | Monthly operating expenses in USD. Must be > 0. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "treasury_sweep_recommender",
  "arguments": {
    "account_balances": {"mercury_checking": 350000, "mercury_savings": 180000},
    "monthly_burn": 42000,
    "operating_buffer_months": 3
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "treasury_sweep_recommender"`.
