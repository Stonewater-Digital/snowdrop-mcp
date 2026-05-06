---
skill: github_trending_scan
category: social
description: Search GitHub for recently active repos in Snowdrop's ecosystem — MCP servers, AI agents, financial tooling, DeFi infrastructure, compliance automation. Returns repos worth watching, potentially starring, or reaching out to.
tier: free
inputs: none
---

# Github Trending Scan

## Description
Search GitHub for recently active repos in Snowdrop's ecosystem — MCP servers, AI agents, financial tooling, DeFi infrastructure, compliance automation. Returns repos worth watching, potentially starring, or reaching out to. Use for ecosystem intelligence and star-for-star trade candidates.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `topics` | `array` | No |  |
| `min_stars` | `integer` | No |  |
| `days_back` | `integer` | No |  |
| `per_query` | `integer` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "github_trending_scan",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "github_trending_scan"`.
