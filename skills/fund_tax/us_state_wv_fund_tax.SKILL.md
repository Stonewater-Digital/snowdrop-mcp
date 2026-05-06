---
skill: us_state_wv_fund_tax
category: fund_tax
description: Computes West Virginia income tax, severance overlays, and elective entity-level tax. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Us State Wv Fund Tax

## Description
Computes West Virginia income tax, severance overlays, and elective entity-level tax. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "us_state_wv_fund_tax",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "us_state_wv_fund_tax"`.
