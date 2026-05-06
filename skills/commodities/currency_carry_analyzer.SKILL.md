---
skill: currency_carry_analyzer
category: commodities
description: Calculates carry yield (interest rate differential) for FX pairs, checks covered interest parity (CIP) deviation against observed forwards, and ranks pairs by carry attractiveness.
tier: free
inputs: pairs
---

# Currency Carry Analyzer

## Description
Calculates carry yield (interest rate differential) for FX pairs, checks covered interest parity (CIP) deviation against observed forwards, and ranks pairs by carry attractiveness.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `pairs` | `array` | Yes | List of FX pair carry inputs. |
| `cip_threshold_pct` | `number` | No | CIP deviation threshold in % to flag arbitrage (default 0.25%). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "currency_carry_analyzer",
  "arguments": {
    "pairs": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "currency_carry_analyzer"`.
