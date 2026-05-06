---
skill: safe_note_converter
category: venture
description: Calculates SAFE conversion price, shares, and founder dilution. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Safe Note Converter

## Description
Calculates SAFE conversion price, shares, and founder dilution. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "safe_note_converter",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "safe_note_converter"`.
