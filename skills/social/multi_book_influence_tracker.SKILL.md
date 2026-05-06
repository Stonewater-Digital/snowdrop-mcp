---
skill: multi_book_influence_tracker
category: social
description: Calculates an agent's influence score across multiple social platforms, identifies top-performing interactions, and infers the influence trend over time.
tier: free
inputs: agent_id, interactions
---

# Multi Book Influence Tracker

## Description
Calculates an agent's influence score across multiple social platforms, identifies top-performing interactions, and infers the influence trend over time.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `agent_id` | `string` | Yes | Unique identifier of the agent being evaluated. |
| `interactions` | `array` | Yes | List of interaction dicts with: platform (str), post_id (str), replies_count (int), citations_count (int), sentiment_impact (float). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "multi_book_influence_tracker",
  "arguments": {
    "agent_id": "<agent_id>",
    "interactions": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "multi_book_influence_tracker"`.
