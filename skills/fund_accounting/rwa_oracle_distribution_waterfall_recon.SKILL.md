---
skill: rwa_oracle_distribution_waterfall_recon
category: fund_accounting
description: Checks that oracle-distributed cashflows match waterfall calculations per tranche. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: payload, context
---

# Rwa Oracle Distribution Waterfall Recon

## Description
Checks that oracle-distributed cashflows match waterfall calculations per tranche. (Premium — subscribe at https://snowdrop.ai)

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `payload` | `object` | Yes | Oracle distribution payload containing tranche-level cashflow data (amounts distributed per tranche, timestamps, and oracle signatures). |
| `context` | `object` | No | Optional reconciliation context, e.g. `{"tolerance_bps": 1, "fund_id": "fund_ii", "period": "Q4 2025"}`. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "rwa_oracle_distribution_waterfall_recon",
  "arguments": {
    "payload": {
      "distribution_id": "dist_20251231_001",
      "total_distributed": 12500000,
      "tranches": [
        {"tranche": "senior_lp", "oracle_amount": 9000000, "waterfall_amount": 9000000},
        {"tranche": "mezzanine_lp", "oracle_amount": 2500000, "waterfall_amount": 2500000},
        {"tranche": "gp_carry", "oracle_amount": 1000000, "waterfall_amount": 1000000}
      ]
    },
    "context": {"tolerance_bps": 1, "fund_id": "rwa_fund_i", "period": "Q4 2025"}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_oracle_distribution_waterfall_recon"`.
