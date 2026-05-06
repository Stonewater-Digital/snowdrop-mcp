---
skill: interest_rate_swap_analyzer
category: derivatives
description: Values a fixed/float interest rate swap and reports DV01 and break-even rate. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Interest Rate Swap Analyzer

## Description
Values a fixed/float interest rate swap and reports DV01 and break-even rate. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "interest_rate_swap_analyzer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "interest_rate_swap_analyzer"`.
