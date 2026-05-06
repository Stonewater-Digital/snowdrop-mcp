---
skill: mica_asset_classification
category: compliance
description: Classifies crypto-assets under EU MiCA Regulation (EU) 2023/1114 as ART (Asset-Referenced Token), EMT (E-Money Token), or Utility Token. Flags significant status based on market cap and daily volume thresholds.
tier: premium
inputs: token_data
---

# Mica Asset Classification

## Description
Classifies crypto-assets under EU MiCA Regulation (EU) 2023/1114 as ART (Asset-Referenced Token), EMT (E-Money Token), or Utility Token. Flags significant status based on market cap and daily volume thresholds. (Premium — subscribe at https://snowdrop.ai)

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `token_data` | `object` | Yes | Token details including reference asset(s), e-money backing, market cap, daily trading volume, and issuer information for MiCA classification |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "mica_asset_classification",
  "arguments": {
    "token_data": {
      "token_name": "EuroStable",
      "reference_assets": ["EUR"],
      "market_cap_eur": 250000000,
      "daily_volume_eur": 8000000,
      "issuer_jurisdiction": "DE"
    }
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "mica_asset_classification"`.
