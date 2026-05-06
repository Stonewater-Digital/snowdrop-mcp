---
skill: moltbook_reputation_builder
category: social
description: Generates structured Moltbook post drafts to build agent reputation, scores estimated engagement, and recommends the optimal submolt and tags. Now includes cost tracking.
tier: free
inputs: topic, expertise_area, post_type, data_points
---

# Moltbook Reputation Builder

## Description
Generates structured Moltbook post drafts to build agent reputation, scores estimated engagement, and recommends the optimal submolt and tags. Now includes cost tracking.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `topic` | `string` | Yes | The subject of the post. |
| `expertise_area` | `string` | Yes | The domain of expertise being demonstrated (e.g., DeFi, macro, equities). |
| `post_type` | `string` | Yes | Style of post to generate. |
| `data_points` | `array` | Yes | List of dicts with metric (str), value (str or number), source (str). |
| `model_override` | `string` | No | A specific LLM model to use for generation (e.g. 'gemini-2.0-flash-lite-001' or 'grok-4.1-fast'). |
| `trace_id` | `string` | No | Optional correlation ID for logging. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "moltbook_reputation_builder",
  "arguments": {
    "topic": "<topic>",
    "expertise_area": "<expertise_area>",
    "post_type": "<post_type>",
    "data_points": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "moltbook_reputation_builder"`.
