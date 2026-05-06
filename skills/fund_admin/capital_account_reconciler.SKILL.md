---
skill: capital_account_reconciler
category: fund_admin
description: Rolls forward an LP capital account from beginning balance with all activity: contributions, distributions, realized gains/losses, unrealized gains/losses, and fees. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: beginning_balance, contributions, distributions, realized_gains, unrealized_gains, fees
---

# Capital Account Reconciler

## Description
Rolls forward an LP capital account from beginning balance with all activity: contributions, distributions, realized gains/losses, unrealized gains/losses, and fees. (Premium — subscribe at https://snowdrop.ai)

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| beginning_balance | number | Yes | Opening LP capital account balance at the start of the period (USD) |
| contributions | number | No | Capital contributions made by the LP during the period (default: 0.0) |
| distributions | number | No | Cash distributions returned to the LP during the period (default: 0.0) |
| realized_gains | number | No | Realized gains (positive) or losses (negative) allocated to this LP (default: 0.0) |
| unrealized_gains | number | No | Change in unrealized appreciation or depreciation allocated to this LP (default: 0.0) |
| fees | number | No | Management fees and fund expenses charged to this LP's account (default: 0.0) |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "capital_account_reconciler",
  "arguments": {
    "beginning_balance": 5000000.00,
    "contributions": 750000.00,
    "distributions": 200000.00,
    "realized_gains": 320000.00,
    "unrealized_gains": 180000.00,
    "fees": 37500.00
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "capital_account_reconciler"`.
