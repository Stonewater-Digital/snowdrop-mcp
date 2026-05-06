---
skill: vote_tabulator
category: governance
description: Counts proposal votes and checks for mandates via 1-sigma upvote threshold.
tier: free
inputs: proposal_id, votes, recent_proposal_stats
---

# Vote Tabulator

## Description
Counts proposal votes and checks for mandates via 1-sigma upvote threshold.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `proposal_id` | `string` | Yes |  |
| `votes` | `array` | Yes |  |
| `recent_proposal_stats` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "vote_tabulator",
  "arguments": {
    "proposal_id": "<proposal_id>",
    "votes": [],
    "recent_proposal_stats": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "vote_tabulator"`.
