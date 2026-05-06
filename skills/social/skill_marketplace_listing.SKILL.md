---
skill: skill_marketplace_listing
category: social
description: Turns the skill registry into a Moltbook/Fragment-friendly markdown listing.
tier: free
inputs: skill_registry
---

# Skill Marketplace Listing

## Description
Turns the skill registry into a Moltbook/Fragment-friendly markdown listing.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `skill_registry` | `object` | Yes | Mapping of skill names to descriptions. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "skill_marketplace_listing",
  "arguments": {
    "skill_registry": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "skill_marketplace_listing"`.
