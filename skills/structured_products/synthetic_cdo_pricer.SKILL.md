---
skill: synthetic_cdo_pricer
category: structured_products
description: Implements the Gaussian copula with Vasicek closed form to deliver expected loss and spreads for each tranche. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Synthetic Cdo Pricer

## Description
Implements the Gaussian copula with Vasicek closed form to deliver expected loss and spreads for each tranche. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "synthetic_cdo_pricer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "synthetic_cdo_pricer"`.
