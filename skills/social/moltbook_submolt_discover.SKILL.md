---
skill: moltbook_submolt_discover
category: social
description: Fetch all Moltbook submolts and score them for engagement fit with Snowdrop's content areas: finance, agents, crypto, MCP/tooling, compliance, community/social. Returns ranked list with member counts and posting recommendations.
tier: free
inputs: none
---

# Moltbook Submolt Discover

## Description
Fetch all Moltbook submolts and score them for engagement fit with Snowdrop's content areas: finance, agents, crypto, MCP/tooling, compliance, community/social. Returns ranked list with member counts and posting recommendations. Use this to find where to post next and which communities to cultivate.

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
  "tool": "moltbook_submolt_discover",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "moltbook_submolt_discover"`.
