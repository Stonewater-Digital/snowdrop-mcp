---
skill: merger_arbitrage_spread
category: alternative_investments
description: Computes dollar and annualized spread along with implied deal probability from price-break analysis. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Merger Arbitrage Spread

## Description
Computes dollar and annualized spread along with implied deal probability from price-break analysis. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "merger_arbitrage_spread",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "merger_arbitrage_spread"`.
