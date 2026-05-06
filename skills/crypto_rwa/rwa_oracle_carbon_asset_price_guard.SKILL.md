---
skill: rwa_oracle_carbon_asset_price_guard
category: crypto_rwa
description: Validates carbon offset price feeds against EU ETS and voluntary market data.
tier: free
inputs: none
---

# Rwa Oracle Carbon Asset Price Guard

## Description
Validates carbon offset price feeds against EU ETS and voluntary market data.

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
  "tool": "rwa_oracle_carbon_asset_price_guard",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_oracle_carbon_asset_price_guard"`.
