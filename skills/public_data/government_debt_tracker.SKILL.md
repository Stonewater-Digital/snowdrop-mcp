---
skill: government_debt_tracker
category: public_data
description: Fetch total US public debt outstanding from the Treasury Fiscal Data API (Debt to the Penny). No API key required.
tier: free
inputs: none
---

# Government Debt Tracker

## Description
Fetch total US public debt outstanding from the Treasury Fiscal Data API (Debt to the Penny). No API key required.

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
  "tool": "government_debt_tracker",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "government_debt_tracker"`.
