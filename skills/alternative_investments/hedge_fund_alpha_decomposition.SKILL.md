---
skill: hedge_fund_alpha_decomposition
category: alternative_investments
description: Performs multi-factor OLS (Fama-French-Carhart) to estimate alpha, betas, R², and information ratio for hedge fund returns. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: fund_returns, factor_returns, risk_free_rate
---

# Hedge Fund Alpha Decomposition

## Description
Performs multi-factor OLS regression (Fama-French-Carhart style) to estimate alpha, factor betas, R², and information ratio for hedge fund returns. Separates manager skill from systematic factor exposure. Premium skill — subscribe at https://snowdrop.ai.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `fund_returns` | `array` | Yes | List of monthly fund net returns as decimals (e.g. [0.015, -0.008, ...]). |
| `factor_returns` | `object` | Yes | Dict mapping factor name to list of corresponding monthly returns (e.g. {"mkt": [...], "smb": [...]}). |
| `risk_free_rate` | `number` | Yes | Monthly risk-free rate as a decimal (e.g. 0.004 for 0.4% per month). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "hedge_fund_alpha_decomposition",
  "arguments": {
    "fund_returns": [0.018, -0.005, 0.022, 0.011, -0.003, 0.014],
    "factor_returns": {
      "mkt": [0.015, -0.010, 0.020, 0.008, -0.005, 0.012],
      "smb": [0.002, 0.001, -0.001, 0.003, 0.000, -0.002]
    },
    "risk_free_rate": 0.004
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "hedge_fund_alpha_decomposition"`.
