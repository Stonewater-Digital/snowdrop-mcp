---
skill: us_state_wa_fund_tax
category: fund_tax
description: Computes Washington capital gains excise exposure for hedge fund allocations and approximates B&O impact. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Us State Wa Fund Tax

## Description
Computes Washington capital gains excise exposure for hedge fund allocations and approximates B&O impact. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "us_state_wa_fund_tax",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "us_state_wa_fund_tax"`.
