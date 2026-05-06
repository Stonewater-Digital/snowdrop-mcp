---
skill: capital_call_notice_generator
category: investor_relations
description: Creates LP-specific capital call instructions awaiting Thunder sign-off. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Capital Call Notice Generator

## Description
Creates LP-specific capital call instructions awaiting Thunder sign-off. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "capital_call_notice_generator",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "capital_call_notice_generator"`.
