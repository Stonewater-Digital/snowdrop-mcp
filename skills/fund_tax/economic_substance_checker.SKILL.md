---
skill: economic_substance_checker
category: fund_tax
description: Checks economic substance requirements for common zero/low-tax fund domiciles. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Economic Substance Checker

## Description
Checks economic substance requirements for common zero/low-tax fund domiciles. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "economic_substance_checker",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "economic_substance_checker"`.
