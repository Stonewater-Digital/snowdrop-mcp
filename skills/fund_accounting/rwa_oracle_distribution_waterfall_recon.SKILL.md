---
skill: rwa_oracle_distribution_waterfall_recon
category: fund_accounting
description: Checks that oracle-distributed cashflows match waterfall calculations per tranche. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Rwa Oracle Distribution Waterfall Recon

## Description
Checks that oracle-distributed cashflows match waterfall calculations per tranche. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "rwa_oracle_distribution_waterfall_recon",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_oracle_distribution_waterfall_recon"`.
