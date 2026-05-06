---
skill: clawback_analyzer
category: fund_accounting
description: Determines whether the GP owes a clawback based on carry received versus carry entitled after preferred return. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Clawback Analyzer

## Description
Determines whether the GP owes a clawback based on carry received versus carry entitled after preferred return. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "clawback_analyzer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "clawback_analyzer"`.
