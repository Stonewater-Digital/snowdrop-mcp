---
skill: certificate_of_deposit_ladder_builder
category: banking
description: Build a CD ladder by dividing a total investment across 1-to-N year CDs. Estimates returns for each rung with a yield curve premium.
tier: free
inputs: total_investment
---

# Certificate Of Deposit Ladder Builder

## Description
Build a CD ladder by dividing a total investment across 1-to-N year CDs. Estimates returns for each rung with a yield curve premium.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `total_investment` | `number` | Yes | Total amount to invest in the ladder. |
| `num_rungs` | `integer` | No | Number of CD rungs (default 5). |
| `base_apy` | `number` | No | APY for a 1-year CD as decimal (default 0.045). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "certificate_of_deposit_ladder_builder",
  "arguments": {
    "total_investment": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "certificate_of_deposit_ladder_builder"`.
