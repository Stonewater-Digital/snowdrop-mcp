---
skill: us_state_nm_fund_tax
category: fund_tax
description: Computes New Mexico income tax, SALT election, and Gross Receipts Tax on management fees. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Us State Nm Fund Tax

## Description
Computes New Mexico income tax, SALT election, and Gross Receipts Tax on management fees. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "us_state_nm_fund_tax",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "us_state_nm_fund_tax"`.
