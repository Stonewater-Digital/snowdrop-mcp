---
skill: convertible_arbitrage_analytics
category: alternative_investments
description: Computes share hedge, gamma exposure, and credit/borrow carry for convert arb positions. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Convertible Arbitrage Analytics

## Description
Computes share hedge, gamma exposure, and credit/borrow carry for convert arb positions. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "convertible_arbitrage_analytics",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "convertible_arbitrage_analytics"`.
