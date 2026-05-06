---
skill: asset_backed_token_collateral_analyr
category: rwa_tokenization
description: Evaluates collateral value, advance rates, and haircuts for asset-backed token programs.
tier: free
inputs: collateral_value, token_outstanding, advance_rate_pct
---

# Asset Backed Token Collateral Analyr

## Description
Evaluates collateral value, advance rates, and haircuts for asset-backed token programs.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `collateral_value` | `number` | Yes | Current collateral market value |
| `token_outstanding` | `number` | Yes | Outstanding token liability |
| `advance_rate_pct` | `number` | Yes | Max allowable advance rate |
| `haircut_pct` | `number` | No | Risk haircut applied to collateral |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "asset_backed_token_collateral_analyr",
  "arguments": {
    "collateral_value": 0,
    "token_outstanding": 0,
    "advance_rate_pct": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "asset_backed_token_collateral_analyr"`.
