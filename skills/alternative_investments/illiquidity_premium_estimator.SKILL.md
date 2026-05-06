---
skill: illiquidity_premium_estimator
category: alternative_investments
description: Computes the Amihud price impact ratio and converts it to an illiquidity premium using Amihud (2002). (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: daily_returns, daily_volume, market_cap
---

# Illiquidity Premium Estimator

## Description
Computes the Amihud price impact ratio from daily returns and dollar volume, then converts it to an estimated illiquidity premium using Amihud (2002) methodology. Useful for private equity discount calibration and liquidity-adjusted CAPM inputs. Premium skill — subscribe at https://snowdrop.ai.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `daily_returns` | `array` | Yes | List of daily return observations as decimals (e.g. [0.01, -0.005, ...]). |
| `daily_volume` | `array` | Yes | List of daily dollar trading volumes corresponding to each return (dollars). |
| `market_cap` | `number` | Yes | Current market capitalization of the security (dollars). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "illiquidity_premium_estimator",
  "arguments": {
    "daily_returns": [0.010, -0.005, 0.008, -0.003, 0.012],
    "daily_volume": [500000, 420000, 610000, 380000, 490000],
    "market_cap": 250000000
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "illiquidity_premium_estimator"`.
