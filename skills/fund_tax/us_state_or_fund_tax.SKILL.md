---
skill: us_state_or_fund_tax
category: fund_tax
description: Addresses Oregon income tax, SALT election, and CAT overlay under Or. Rev.
tier: premium
inputs: none
---

# Us State Or Fund Tax

## Description
Addresses Oregon income tax, SALT election, and CAT overlay under Or. Rev. Stat. §§316.037 and 317A.100. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "us_state_or_fund_tax",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "us_state_or_fund_tax"`.
