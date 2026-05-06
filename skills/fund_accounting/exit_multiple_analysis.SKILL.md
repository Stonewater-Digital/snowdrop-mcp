---
skill: exit_multiple_analysis
category: fund_accounting
description: Analyzes a portfolio of realized exits to compute Money-on-Invested-Capital (MoIC) multiples for each position. Aggregates median, mean, min, and max multiples at the portfolio level and breaks down performance by sector and exit type (IPO, M&A, secondary, write-off, etc.).
tier: premium
inputs: none
---

# Exit Multiple Analysis

## Description
Analyzes a portfolio of realized exits to compute Money-on-Invested-Capital (MoIC) multiples for each position. Aggregates median, mean, min, and max multiples at the portfolio level and breaks down performance by sector and exit type (IPO, M&A, secondary, write-off, etc.). (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "exit_multiple_analysis",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "exit_multiple_analysis"`.
