---
skill: us_state_ca_fund_tax
category: fund_tax
description: Models California PIT, LLC fee, nonresident withholding, and AB 150 pass-through entity tax under Cal. Rev.
tier: premium
inputs: none
---

# Us State Ca Fund Tax

## Description
Models California PIT, LLC fee, nonresident withholding, and AB 150 pass-through entity tax under Cal. Rev. & Tax. Code §§17041, 17942, 18662, and 19900. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "us_state_ca_fund_tax",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "us_state_ca_fund_tax"`.
