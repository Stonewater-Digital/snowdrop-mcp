---
skill: debt_covenant_monitor
category: fund_accounting
description: Evaluates debt covenants against current financial ratios. Supports leverage_ratio (lower is better), interest_coverage (higher is better), and current_ratio (higher is better) covenant types.
tier: premium
inputs: none
---

# Debt Covenant Monitor

## Description
Evaluates debt covenants against current financial ratios. Supports leverage_ratio (lower is better), interest_coverage (higher is better), and current_ratio (higher is better) covenant types. Returns breach status and distance-to-breach for each covenant. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "debt_covenant_monitor",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "debt_covenant_monitor"`.
