---
skill: ubti_blocker_analyzer
category: fund_tax
description: Computes unrelated business taxable income under IRC §§512-514 and recommends blocker structures. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Ubti Blocker Analyzer

## Description
Computes unrelated business taxable income under IRC §§512-514 and recommends blocker structures. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "ubti_blocker_analyzer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "ubti_blocker_analyzer"`.
