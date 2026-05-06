---
skill: synthetic_market_data_generator
category: data_ingestion
description: Generates realistic synthetic market data (time series, spreads, curves) for free-tier advanced analytics skills.
tier: free
inputs: none
---

# Synthetic Market Data Generator

## Description
Generates realistic synthetic market data (time series, spreads, curves) for free-tier advanced analytics skills.

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
  "tool": "synthetic_market_data_generator",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "synthetic_market_data_generator"`.
