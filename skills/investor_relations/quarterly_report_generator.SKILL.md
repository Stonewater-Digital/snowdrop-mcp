---
skill: quarterly_report_generator
category: investor_relations
description: Summarizes fund performance against benchmarks for the quarter. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Quarterly Report Generator

## Description
Summarizes fund performance against benchmarks for the quarter. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "quarterly_report_generator",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "quarterly_report_generator"`.
