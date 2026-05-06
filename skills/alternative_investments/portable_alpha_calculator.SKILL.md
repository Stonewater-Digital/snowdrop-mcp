---
skill: portable_alpha_calculator
category: alternative_investments
description: Aggregates returns from alpha and beta sleeves, subtracts hedge cost, and reports contribution along with realized tracking error. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Portable Alpha Calculator

## Description
Aggregates returns from alpha and beta sleeves, subtracts hedge cost, and reports contribution along with realized tracking error. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "portable_alpha_calculator",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "portable_alpha_calculator"`.
