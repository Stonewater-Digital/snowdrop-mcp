---
skill: usd_jpy_carry_trade_monitor
category: fx
description: Analyzes USD/JPY carry trade profitability using US vs Japan yield differentials and synthetic FX volatility.
tier: free
inputs: none
---

# Usd Jpy Carry Trade Monitor

## Description
Analyzes USD/JPY carry trade profitability using US vs Japan yield differentials and synthetic FX volatility.

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
  "tool": "usd_jpy_carry_trade_monitor",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "usd_jpy_carry_trade_monitor"`.
