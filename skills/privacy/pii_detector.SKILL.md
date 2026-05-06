---
skill: pii_detector
category: privacy
description: Finds PII in free-form text and masks the findings.
tier: free
inputs: text
---

# Pii Detector

## Description
Finds PII in free-form text and masks the findings.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `text` | `string` | Yes |  |
| `check_types` | `array` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "pii_detector",
  "arguments": {
    "text": "<text>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "pii_detector"`.
