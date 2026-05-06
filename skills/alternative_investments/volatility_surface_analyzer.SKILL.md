---
skill: volatility_surface_analyzer
category: alternative_investments
description: Regresses implied volatility against strikes for each expiry to measure skew and term structure. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: option_chain
---

# Volatility Surface Analyzer

## Description
Regresses implied volatility against moneyness for each expiry to measure skew slope, term structure, and ATM vol term premium. Identifies skew anomalies and vol surface arbitrage opportunities. Premium skill — subscribe at https://snowdrop.ai.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `option_chain` | `array` | Yes | List of option objects, each with fields: `strike`, `expiry_days`, `implied_vol`, `option_type` ("call"/"put"), `spot_price`. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "volatility_surface_analyzer",
  "arguments": {
    "option_chain": [
      {"strike": 95.0, "expiry_days": 30, "implied_vol": 0.28, "option_type": "put", "spot_price": 100.0},
      {"strike": 100.0, "expiry_days": 30, "implied_vol": 0.22, "option_type": "call", "spot_price": 100.0},
      {"strike": 105.0, "expiry_days": 30, "implied_vol": 0.20, "option_type": "call", "spot_price": 100.0},
      {"strike": 95.0, "expiry_days": 60, "implied_vol": 0.26, "option_type": "put", "spot_price": 100.0},
      {"strike": 100.0, "expiry_days": 60, "implied_vol": 0.23, "option_type": "call", "spot_price": 100.0}
    ]
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "volatility_surface_analyzer"`.
