---
skill: feedback_sentiment_analyzer
category: feedback
description: Computes sentiment trends and common themes from feedback entries.
tier: free
inputs: feedback_entries
---

# Feedback Sentiment Analyzer

## Description
Computes sentiment trends and common themes from feedback entries.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `feedback_entries` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "feedback_sentiment_analyzer",
  "arguments": {
    "feedback_entries": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "feedback_sentiment_analyzer"`.
