---
skill: us_state_az_fund_tax
category: fund_tax
description: Calculates Arizona pass-through entity tax, Form 165 withholding, and composite filing tests under Ariz. Rev.
tier: premium
inputs: none
---

# Us State Az Fund Tax

## Description
Calculates Arizona pass-through entity tax, Form 165 withholding, and composite filing tests under Ariz. Rev. Stat. §§43-1011 and 43-1147. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "us_state_az_fund_tax",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "us_state_az_fund_tax"`.
