---
skill: fund_of_funds_allocator
category: fund_accounting
description: Creates a heuristic allocation maximizing expected return under diversification rules. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Fund Of Funds Allocator

## Description
Creates a heuristic allocation maximizing expected return under diversification rules. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "fund_of_funds_allocator",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "fund_of_funds_allocator"`.
