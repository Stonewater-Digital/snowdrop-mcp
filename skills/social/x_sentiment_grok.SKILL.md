---
skill: x_sentiment_grok
category: social
description: Constructs xAI Grok payloads for sentiment queries.
tier: free
inputs: query, timeframe_hours
---

# X Sentiment Grok

## Description
Constructs xAI Grok payloads for sentiment queries.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `query` | `string` | Yes |  |
| `timeframe_hours` | `integer` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "x_sentiment_grok",
  "arguments": {
    "query": "<query>",
    "timeframe_hours": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "x_sentiment_grok"`.
