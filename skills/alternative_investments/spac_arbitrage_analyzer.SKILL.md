---
skill: spac_arbitrage_analyzer
category: alternative_investments
description: Breaks down SPAC trust yield, deal optionality, and expected value based on probability inputs. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: spac_price, trust_value, days_to_redemption, deal_probability, warrant_value
---

# SPAC Arbitrage Analyzer

## Description
Breaks down SPAC trust yield, deal optionality, and expected value given deal probability inputs. Computes annualized trust yield, probability-weighted return, and warrant contribution to total value. Premium skill — subscribe at https://snowdrop.ai.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `spac_price` | `number` | Yes | Current SPAC unit or share market price (dollars). |
| `trust_value` | `number` | Yes | Per-share trust account value (dollars, typically near $10). |
| `days_to_redemption` | `integer` | Yes | Estimated days until redemption deadline or deal close. |
| `deal_probability` | `number` | Yes | Estimated probability of a successful deal announcement (0–1). |
| `warrant_value` | `number` | Yes | Current market value of the warrant component per unit (dollars). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "spac_arbitrage_analyzer",
  "arguments": {
    "spac_price": 9.85,
    "trust_value": 10.10,
    "days_to_redemption": 120,
    "deal_probability": 0.65,
    "warrant_value": 0.45
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "spac_arbitrage_analyzer"`.
