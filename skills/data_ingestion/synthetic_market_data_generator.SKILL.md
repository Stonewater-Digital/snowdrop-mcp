---
skill: synthetic_market_data_generator
category: data_ingestion
description: Generates realistic synthetic market data (time series, spreads, curves) for free-tier advanced analytics skills.
tier: free
inputs: asset_class, data_type
---

# Synthetic Market Data Generator

## Description
Generates realistic synthetic market data (time series, spreads, curves) for free-tier advanced analytics skills.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `asset_class` | `string` | Yes |  |
| `data_type` | `string` | Yes |  |
| `days_back` | `integer` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "synthetic_market_data_generator",
  "arguments": {
    "asset_class": "<asset_class>",
    "data_type": "<data_type>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "synthetic_market_data_generator"`.
