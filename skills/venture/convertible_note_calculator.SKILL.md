---
skill: convertible_note_calculator
category: venture
description: Computes accrued interest, conversion price, and shares for convertible notes. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Convertible Note Calculator

## Description
Computes accrued interest, conversion price, and shares for convertible notes. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "convertible_note_calculator",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "convertible_note_calculator"`.
