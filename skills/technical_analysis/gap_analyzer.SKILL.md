---
skill: gap_analyzer
category: technical_analysis
description: Scans OHLC data for breakaway, runaway, exhaustion, and common gaps, tracking fill status.
tier: free
inputs: opens, highs, lows, closes
---

# Gap Analyzer

## Description
Scans OHLC data for breakaway, runaway, exhaustion, and common gaps, tracking fill status.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `opens` | `array` | Yes | Open prices. |
| `highs` | `array` | Yes | High prices. |
| `lows` | `array` | Yes | Low prices. |
| `closes` | `array` | Yes | Close prices. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "gap_analyzer",
  "arguments": {
    "opens": [],
    "highs": [],
    "lows": [],
    "closes": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "gap_analyzer"`.
