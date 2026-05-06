---
skill: venture_return_analyzer
category: venture
description: Computes proceeds for preferred vs common across exit scenarios, including participation caps. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Venture Return Analyzer

## Description
Computes proceeds for preferred vs common across exit scenarios, including participation caps. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "venture_return_analyzer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "venture_return_analyzer"`.
