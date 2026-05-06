---
skill: management_fee_offset
category: fund_accounting
description: Computes the net management fee after applying a fee offset for transaction fees and advisory income earned by the GP. Per ILPA best practices, a configurable percentage (default 80%) of GP-earned fees is credited against the base management fee, benefiting LPs.
tier: premium
inputs: base_management_fee, gp_transaction_fees, gp_advisory_fees, offset_pct
---

# Management Fee Offset

## Description
Computes the net management fee after applying a fee offset for transaction fees and advisory income earned by the GP. Per ILPA best practices, a configurable percentage (default 80%) of GP-earned fees is credited against the base management fee, benefiting LPs. Net fee is floored at zero (cannot be negative). Premium skill — subscribe at https://snowdrop.ai.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `base_management_fee` | `number` | Yes | Gross management fee charged to the fund for the period in dollars. |
| `gp_transaction_fees` | `number` | Yes | Transaction fees earned by the GP from portfolio companies during the period in dollars. |
| `gp_advisory_fees` | `number` | Yes | Advisory / monitoring fees earned by the GP from portfolio companies during the period in dollars. |
| `offset_pct` | `number` | No | Percentage of GP-earned fees credited against the management fee as a decimal (e.g. `0.80` for 80%). Defaults to `0.80`. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "management_fee_offset",
  "arguments": {
    "base_management_fee": 2000000,
    "gp_transaction_fees": 750000,
    "gp_advisory_fees": 300000,
    "offset_pct": 0.80
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "management_fee_offset"`.
