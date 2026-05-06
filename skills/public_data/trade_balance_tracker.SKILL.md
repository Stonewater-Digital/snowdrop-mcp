---
skill: trade_balance_tracker
category: public_data
description: Track the US trade balance (goods and services) from FRED (series BOPGSTB). Returns latest value.
tier: free
inputs: none
---

# Trade Balance Tracker

## Description
Track the US trade balance (goods and services) from FRED (series BOPGSTB). Returns latest value. Requires FRED_API_KEY.

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
  "tool": "trade_balance_tracker",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "trade_balance_tracker"`.
