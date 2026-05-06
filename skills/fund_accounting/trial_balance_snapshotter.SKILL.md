---
skill: trial_balance_snapshotter
category: fund_accounting
description: Converts ledger entries into a base-currency trial balance and highlights NAV deltas. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Trial Balance Snapshotter

## Description
Converts ledger entries into a base-currency trial balance and highlights NAV deltas. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "trial_balance_snapshotter",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "trial_balance_snapshotter"`.
