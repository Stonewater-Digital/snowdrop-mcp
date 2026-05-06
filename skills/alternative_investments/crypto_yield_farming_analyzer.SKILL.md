---
skill: crypto_yield_farming_analyzer
category: alternative_investments
description: Converts pool volume/TVL and token incentives into APY while quantifying impermanent loss via volatility. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Crypto Yield Farming Analyzer

## Description
Converts pool volume/TVL and token incentives into APY while quantifying impermanent loss via volatility. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "crypto_yield_farming_analyzer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "crypto_yield_farming_analyzer"`.
