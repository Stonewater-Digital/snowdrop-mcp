---
skill: financial_content_draft
category: social
description: Generate high-quality financial content in Snowdrop's voice: market commentary, regulatory explainers (MiCA, GDPR, FinCEN BOIR, SEC Reg BI, SEBI FPI, etc.), DeFi mechanics breakdowns, compliance checklists, or portfolio analysis narratives. Content is designed to be genuinely useful and establish Snowdrop as an authority in agent finance.
tier: free
inputs: none
---

# Financial Content Draft

## Description
Generate high-quality financial content in Snowdrop's voice: market commentary, regulatory explainers (MiCA, GDPR, FinCEN BOIR, SEC Reg BI, SEBI FPI, etc.), DeFi mechanics breakdowns, compliance checklists, or portfolio analysis narratives. Content is designed to be genuinely useful and establish Snowdrop as an authority in agent finance. Includes a platform-appropriate version (GitHub, Moltbook, X/Twitter).

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
  "tool": "financial_content_draft",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "financial_content_draft"`.
