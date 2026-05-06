---
skill: convexity_hedger
category: fixed_income_analytics
description: Determines barbell weights that match the duration of a bullet bond while maximizing convexity per CFA curriculum. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Convexity Hedger

## Description
Determines barbell weights that match the duration of a bullet bond while maximizing convexity per CFA curriculum. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "convexity_hedger",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "convexity_hedger"`.
