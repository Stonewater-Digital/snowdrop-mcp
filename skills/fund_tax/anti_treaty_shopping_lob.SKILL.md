---
skill: anti_treaty_shopping_lob
category: fund_tax
description: Evaluates LOB tests (ownership/base erosion, publicly traded, active trade or business, derivative benefits). (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Anti Treaty Shopping Lob

## Description
Evaluates LOB tests (ownership/base erosion, publicly traded, active trade or business, derivative benefits). (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "anti_treaty_shopping_lob",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "anti_treaty_shopping_lob"`.
