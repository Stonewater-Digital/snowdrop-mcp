---
skill: moltbook_sentiment_analyzer
category: social
description: Scores Moltbook posts for financial sentiment and detects narrative shifts within submolts over a configurable lookback window.
tier: free
inputs: posts
---

# Moltbook Sentiment Analyzer

## Description
Scores Moltbook posts for financial sentiment and detects narrative shifts within submolts over a configurable lookback window.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `posts` | `array` | Yes | List of post dicts with keys: author (str), content (str), timestamp (ISO-8601 str), upvotes (int), submolt (str). |
| `lookback_hours` | `integer` | No | How many hours back to include in the analysis window. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "moltbook_sentiment_analyzer",
  "arguments": {
    "posts": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "moltbook_sentiment_analyzer"`.
