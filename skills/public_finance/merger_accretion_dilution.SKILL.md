---
skill: merger_accretion_dilution
category: public_finance
description: Evaluates EPS impact of an acquisition with cash/stock mix and synergies.
tier: free
inputs: acquirer, target, offer_premium_pct, payment_mix, synergies, financing_rate, tax_rate
---

# Merger Accretion Dilution

## Description
Evaluates EPS impact of an acquisition with cash/stock mix and synergies.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `acquirer` | `object` | Yes |  |
| `target` | `object` | Yes |  |
| `offer_premium_pct` | `number` | Yes |  |
| `payment_mix` | `object` | Yes |  |
| `synergies` | `number` | Yes |  |
| `financing_rate` | `number` | Yes |  |
| `tax_rate` | `number` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "merger_accretion_dilution",
  "arguments": {
    "acquirer": {},
    "target": {},
    "offer_premium_pct": 0,
    "payment_mix": {},
    "synergies": 0,
    "financing_rate": 0,
    "tax_rate": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "merger_accretion_dilution"`.
