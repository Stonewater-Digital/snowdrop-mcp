---
skill: places_search
category: root
description: Search, discover, and retrieve details for businesses and points of interest using the Google Places API (New). Supports free-text search, nearby discovery, and full place detail lookups.
tier: free
inputs: action
---

# Places Search

## Description
Search, discover, and retrieve details for businesses and points of interest using the Google Places API (New). Supports free-text search, nearby discovery, and full place detail lookups. Returns structured business data plus an investment_signal field assessing business density and health for real estate and market analysis.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `action` | `string` | Yes | Places operation to perform. |
| `query` | `string` | No | Free-text search query (search action). |
| `place_id` | `string` | No | Google Place ID for detail lookup (details action). |
| `location` | `string` | No | 'lat,lng' string used to bias search or anchor nearby (nearby/search actions). |
| `radius_meters` | `integer` | No | Search radius in meters for nearby action. |
| `type` | `string` | No | Place type filter (e.g. 'restaurant', 'bank', 'real_estate_agency'). |
| `max_results` | `integer` | No | Maximum number of places to return (1–20). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "places_search",
  "arguments": {
    "action": "<action>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "places_search"`.
