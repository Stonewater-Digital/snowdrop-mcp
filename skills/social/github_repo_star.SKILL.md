---
skill: github_repo_star
category: social
description: Star or unstar a GitHub repository as the authenticated user (Snowdrop-Apex). Use for star-for-star trades with community members, or to signal appreciation for repos that are genuinely useful.
tier: free
inputs: none
---

# Github Repo Star

## Description
Star or unstar a GitHub repository as the authenticated user (Snowdrop-Apex). Use for star-for-star trades with community members, or to signal appreciation for repos that are genuinely useful. Also returns current star count for a repo.

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
  "tool": "github_repo_star",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "github_repo_star"`.
