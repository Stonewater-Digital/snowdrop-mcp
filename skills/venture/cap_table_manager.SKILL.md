---
skill: cap_table_manager
category: venture
description: Computes fully diluted ownership after venture rounds including option pools and notes. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Cap Table Manager

## Description
Computes fully diluted ownership after venture rounds including option pools and notes. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "cap_table_manager",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "cap_table_manager"`.
