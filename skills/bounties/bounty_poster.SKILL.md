---
skill: bounty_poster
category: bounties
description: Publishes new skill, feature, or bug-fix bounties to the community board.
tier: free
inputs: title, description, reward_amount, reward_currency, category, difficulty
---

# Bounty Poster

## Description
Publishes new skill, feature, or bug-fix bounties to the community board.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `title` | `string` | Yes |  |
| `description` | `string` | Yes |  |
| `reward_amount` | `number` | Yes |  |
| `reward_currency` | `string` | Yes |  |
| `category` | `string` | Yes |  |
| `deadline` | `['string', 'null']` | No |  |
| `difficulty` | `string` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "bounty_poster",
  "arguments": {
    "title": "<title>",
    "description": "<description>",
    "reward_amount": 0,
    "reward_currency": "<reward_currency>",
    "category": "<category>",
    "difficulty": "<difficulty>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "bounty_poster"`.
