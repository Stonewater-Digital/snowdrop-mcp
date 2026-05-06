---
skill: capital_account_reconciler
category: fund_admin
description: Rolls forward an LP capital account from beginning balance with all activity: contributions, distributions, realized gains/losses, unrealized gains/losses, and fees. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Capital Account Reconciler

## Description
Rolls forward an LP capital account from beginning balance with all activity: contributions, distributions, realized gains/losses, unrealized gains/losses, and fees. (Premium — subscribe at https://snowdrop.ai)

## Parameters
_No parameters defined._

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "capital_account_reconciler",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "capital_account_reconciler"`.
