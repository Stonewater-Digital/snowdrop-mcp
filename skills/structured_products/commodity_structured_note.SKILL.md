---
skill: commodity_structured_note
category: structured_products
description: Values a participation note written on a commodity forward using Black's model and applies cap/floor constraints. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Commodity Structured Note

## Description
Values a participation note written on a commodity forward using Black's model and applies cap/floor constraints. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "commodity_structured_note",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "commodity_structured_note"`.
