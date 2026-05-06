---
skill: mica_asset_classification
category: compliance
description: Classifies crypto-assets under EU MiCA Regulation (EU) 2023/1114 as ART (Asset-Referenced Token), EMT (E-Money Token), or Utility Token. Flags significant status based on market cap and daily volume thresholds.
tier: premium
inputs: none
---

# Mica Asset Classification

## Description
Classifies crypto-assets under EU MiCA Regulation (EU) 2023/1114 as ART (Asset-Referenced Token), EMT (E-Money Token), or Utility Token. Flags significant status based on market cap and daily volume thresholds. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "mica_asset_classification",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "mica_asset_classification"`.
