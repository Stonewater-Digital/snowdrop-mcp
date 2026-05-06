---
skill: statistical_arbitrage_zscore
category: alternative_investments
description: Performs OLS regression of X on Y to compute hedge ratio, z-score, and Ornstein-Uhlenbeck half-life for pairs trading. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Statistical Arbitrage Zscore

## Description
Performs OLS regression of X on Y to compute hedge ratio, z-score, and Ornstein-Uhlenbeck half-life for pairs trading. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "statistical_arbitrage_zscore",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "statistical_arbitrage_zscore"`.
