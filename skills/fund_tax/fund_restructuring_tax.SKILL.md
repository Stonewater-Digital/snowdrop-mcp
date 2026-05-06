---
skill: fund_restructuring_tax
category: fund_tax
description: Evaluates IRC §§351, 368, 367 and EU Merger Directive treatment for fund Merger/Domestication transactions. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Fund Restructuring Tax

## Description
Evaluates IRC §§351, 368, 367 and EU Merger Directive treatment for fund Merger/Domestication transactions. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "fund_restructuring_tax",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "fund_restructuring_tax"`.
