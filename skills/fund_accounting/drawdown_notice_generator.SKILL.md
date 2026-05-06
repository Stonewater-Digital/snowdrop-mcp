---
skill: drawdown_notice_generator
category: fund_accounting
description: Produce structured LP drawdown notices and routing metadata. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Drawdown Notice Generator

## Description
Produce structured LP drawdown notices and routing metadata. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "drawdown_notice_generator",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "drawdown_notice_generator"`.
