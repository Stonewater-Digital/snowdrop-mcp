---
skill: dao_governance_participation_scorer
category: smart_contracts
description: Assesses voter turnout and proposal engagement to highlight DAO governance strength.
tier: free
inputs: eligible_votes, votes_cast, proposals_total, proposals_participated
---

# Dao Governance Participation Scorer

## Description
Assesses voter turnout and proposal engagement to highlight DAO governance strength.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `eligible_votes` | `number` | Yes | Total votes that could have been cast |
| `votes_cast` | `number` | Yes | Actual votes submitted |
| `proposals_total` | `integer` | Yes | Proposals during the measurement window |
| `proposals_participated` | `integer` | Yes | Number of proposals with quorum participation |
| `quorum_threshold_pct` | `number` | No | Quorum percentage target |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "dao_governance_participation_scorer",
  "arguments": {
    "eligible_votes": 0,
    "votes_cast": 0,
    "proposals_total": 0,
    "proposals_participated": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "dao_governance_participation_scorer"`.
