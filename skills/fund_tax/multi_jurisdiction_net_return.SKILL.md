---
skill: multi_jurisdiction_net_return
category: fund_tax
description: Combines treaty withholding, local fund tax, and investor-level tax drag across income types. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Multi Jurisdiction Net Return

## Description
Combines treaty withholding, local fund tax, and investor-level tax drag across income types. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "multi_jurisdiction_net_return",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "multi_jurisdiction_net_return"`.
