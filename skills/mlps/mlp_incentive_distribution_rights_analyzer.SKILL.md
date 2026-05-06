---
skill: mlp_incentive_distribution_rights_analyzer
category: mlps
description: Applies MLP IDR tiers to calculate GP vs LP cash splits at current distribution rates. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Mlp Incentive Distribution Rights Analyzer

## Description
Applies MLP IDR tiers to calculate GP vs LP cash splits at current distribution rates. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "mlp_incentive_distribution_rights_analyzer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "mlp_incentive_distribution_rights_analyzer"`.
