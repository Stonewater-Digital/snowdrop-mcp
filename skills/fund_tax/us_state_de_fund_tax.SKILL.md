---
skill: us_state_de_fund_tax
category: fund_tax
description: Tracks Delaware intangible exemption status and annual LP/LLC franchise tax even though no entity-level income tax applies to qualified investment funds. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Us State De Fund Tax

## Description
Tracks Delaware intangible exemption status and annual LP/LLC franchise tax even though no entity-level income tax applies to qualified investment funds. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "us_state_de_fund_tax",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "us_state_de_fund_tax"`.
