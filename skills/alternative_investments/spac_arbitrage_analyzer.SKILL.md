---
skill: spac_arbitrage_analyzer
category: alternative_investments
description: Breaks down SPAC trust yield, deal optionality, and expected value based on probability inputs. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Spac Arbitrage Analyzer

## Description
Breaks down SPAC trust yield, deal optionality, and expected value based on probability inputs. (Premium — subscribe at https://snowdrop.ai)

## Parameters
_No parameters defined._

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "spac_arbitrage_analyzer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "spac_arbitrage_analyzer"`.
