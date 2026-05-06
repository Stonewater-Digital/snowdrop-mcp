---
skill: intl_au_fund_tax
category: fund_tax
description: Computes Australian dividend/interest/royalty withholding, MIT incentives, and 30% corporate tax for onshore management entities. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Intl Au Fund Tax

## Description
Computes Australian dividend/interest/royalty withholding, MIT incentives, and 30% corporate tax for onshore management entities. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "intl_au_fund_tax",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "intl_au_fund_tax"`.
