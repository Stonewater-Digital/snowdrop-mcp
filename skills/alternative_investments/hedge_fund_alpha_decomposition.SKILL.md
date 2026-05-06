---
skill: hedge_fund_alpha_decomposition
category: alternative_investments
description: Performs multi-factor OLS (Fama-French-Carhart) to estimate alpha, betas, R², and information ratio for hedge fund returns. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Hedge Fund Alpha Decomposition

## Description
Performs multi-factor OLS (Fama-French-Carhart) to estimate alpha, betas, R², and information ratio for hedge fund returns. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "hedge_fund_alpha_decomposition",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "hedge_fund_alpha_decomposition"`.
