---
skill: us_state_ar_fund_tax
category: fund_tax
description: Applies Arkansas top individual rate, SALT workaround election, and nonresident withholding needed under Ark. Code §26-51-919.
tier: premium
inputs: none
---

# Us State Ar Fund Tax

## Description
Applies Arkansas top individual rate, SALT workaround election, and nonresident withholding needed under Ark. Code §26-51-919. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "us_state_ar_fund_tax",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "us_state_ar_fund_tax"`.
