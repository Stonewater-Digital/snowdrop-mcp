---
skill: us_state_mi_fund_tax
category: fund_tax
description: Runs Michigan flow-through tax computations including nonresident withholding consistency with Mich. Comp.
tier: premium
inputs: none
---

# Us State Mi Fund Tax

## Description
Runs Michigan flow-through tax computations including nonresident withholding consistency with Mich. Comp. Laws §§206.51 and 206.325. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "us_state_mi_fund_tax",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "us_state_mi_fund_tax"`.
