---
skill: schedule_d_8949_generator
category: compliance
description: Classifies transactions into short- and long-term gains for tax filing. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Schedule D 8949 Generator

## Description
Classifies transactions into short- and long-term gains for tax filing. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "schedule_d_8949_generator",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "schedule_d_8949_generator"`.
