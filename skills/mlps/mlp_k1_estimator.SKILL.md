---
skill: mlp_k1_estimator
category: mlps
description: Estimates income, return of capital, and UBTI exposure for MLP units. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Mlp K1 Estimator

## Description
Estimates income, return of capital, and UBTI exposure for MLP units. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "mlp_k1_estimator",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "mlp_k1_estimator"`.
