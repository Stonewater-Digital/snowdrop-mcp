---
skill: commodity_index_fetcher
category: public_data
description: Fetch commodity price data from FRED. Supports: gold, silver, oil/wti, brent, natural_gas, copper, aluminum, wheat, corn, cotton, sugar, coffee.
tier: free
inputs: none
---

# Commodity Index Fetcher

## Description
Fetch commodity price data from FRED. Supports: gold, silver, oil/wti, brent, natural_gas, copper, aluminum, wheat, corn, cotton, sugar, coffee. Requires FRED_API_KEY.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `commodity` | `string` | No | Commodity name (e.g., 'gold', 'oil', 'copper', 'wheat'). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "commodity_index_fetcher",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "commodity_index_fetcher"`.
