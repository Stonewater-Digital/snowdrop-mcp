---
skill: pillar_3_disclosure_generator
category: regulatory_capital
description: Prepares Pillar 3 style summary of capital ratios, RWAs, LCR/NSFR, and leverage metrics.
tier: free
inputs: capital, rwa_by_risk_type, liquidity_metrics, leverage_ratio_pct
---

# Pillar 3 Disclosure Generator

## Description
Prepares Pillar 3 style summary of capital ratios, RWAs, LCR/NSFR, and leverage metrics.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `capital` | `object` | Yes | Capital amounts (CET1, Tier1, Total). |
| `rwa_by_risk_type` | `object` | Yes | RWA amounts per risk type. |
| `liquidity_metrics` | `object` | Yes | Liquidity ratios (LCR, NSFR). |
| `leverage_ratio_pct` | `number` | Yes | Basel leverage ratio. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "pillar_3_disclosure_generator",
  "arguments": {
    "capital": {},
    "rwa_by_risk_type": {},
    "liquidity_metrics": {},
    "leverage_ratio_pct": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "pillar_3_disclosure_generator"`.
