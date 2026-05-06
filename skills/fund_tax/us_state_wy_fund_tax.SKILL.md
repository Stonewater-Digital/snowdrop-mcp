---
skill: us_state_wy_fund_tax
category: fund_tax
description: Tracks Wyoming annual license tax exposure for holding entities. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Us State Wy Fund Tax

## Description
Tracks Wyoming annual license tax exposure for holding entities. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "us_state_wy_fund_tax",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "us_state_wy_fund_tax"`.
