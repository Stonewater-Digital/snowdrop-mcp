---
skill: us_state_ky_fund_tax
category: fund_tax
description: Aggregates Kentucky income tax, LLET, and composite filing logic under KRS 141.020 and 141.0401. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Us State Ky Fund Tax

## Description
Aggregates Kentucky income tax, LLET, and composite filing logic under KRS 141.020 and 141.0401. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "us_state_ky_fund_tax",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "us_state_ky_fund_tax"`.
