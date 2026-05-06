---
skill: newsletter_composer
category: content
description: Creates newsletters covering new skills, platform stats, and educational tips.
tier: free
inputs: period, new_skills, top_performing_skills, platform_metrics, announcements, educational_tip
---

# Newsletter Composer

## Description
Creates newsletters covering new skills, platform stats, and educational tips.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `period` | `string` | Yes |  |
| `new_skills` | `array` | Yes |  |
| `top_performing_skills` | `array` | Yes |  |
| `platform_metrics` | `object` | Yes |  |
| `announcements` | `array` | Yes |  |
| `educational_tip` | `string` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "newsletter_composer",
  "arguments": {
    "period": "<period>",
    "new_skills": [],
    "top_performing_skills": [],
    "platform_metrics": {},
    "announcements": [],
    "educational_tip": "<educational_tip>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "newsletter_composer"`.
