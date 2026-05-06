---
skill: cdo_tranche_pricer
category: structured_products
description: Prices a CDO tranche using the Li (2000) Gaussian copula and Vasicek LHP model to deliver expected loss, spread, and delta analytics. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Cdo Tranche Pricer

## Description
Prices a CDO tranche using the Li (2000) Gaussian copula and Vasicek LHP model to deliver expected loss, spread, and delta analytics. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "cdo_tranche_pricer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "cdo_tranche_pricer"`.
