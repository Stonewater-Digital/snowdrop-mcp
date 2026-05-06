---
skill: total_return_swap_analyzer
category: derivatives
description: Breaks down TRS financing costs, received return, and net P&L. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Total Return Swap Analyzer

## Description
Breaks down TRS financing costs, received return, and net P&L. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "total_return_swap_analyzer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "total_return_swap_analyzer"`.
