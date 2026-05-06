---
skill: ecosystem_radar
category: social
description: Scan the MCP, autonomous agent, and DeFi finance ecosystem for recent developments: new MCP servers, agent frameworks, regulatory changes, competitor moves, and emerging communities. Returns a digest of what's happening so Snowdrop can engage with context and intelligence rather than posting into the void.
tier: free
inputs: none
---

# Ecosystem Radar

## Description
Scan the MCP, autonomous agent, and DeFi finance ecosystem for recent developments: new MCP servers, agent frameworks, regulatory changes, competitor moves, and emerging communities. Returns a digest of what's happening so Snowdrop can engage with context and intelligence rather than posting into the void.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `search_terms` | `array` | No |  |
| `use_github_search` | `boolean` | No |  |
| `use_web_search` | `boolean` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "ecosystem_radar",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "ecosystem_radar"`.
