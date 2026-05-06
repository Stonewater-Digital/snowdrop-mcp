---
skill: agent_skill_version_checker
category: technical
description: Verifies Context7 documentation freshness for registered skills. Flags any skill whose last_checked date is older than 7 days and returns a freshness score as a percentage of up-to-date skills.
tier: free
inputs: skills
---

# Agent Skill Version Checker

## Description
Verifies Context7 documentation freshness for registered skills. Flags any skill whose last_checked date is older than 7 days and returns a freshness score as a percentage of up-to-date skills.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `skills` | `array` | Yes | List of skill descriptors with version and last-checked timestamp. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "agent_skill_version_checker",
  "arguments": {
    "skills": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "agent_skill_version_checker"`.
