---
skill: esg_sfdr_categorization
category: compliance
description: Classifies EU investment funds under SFDR (EU) 2019/2088 as Article 6 (no ESG), Article 8 (promotes ESG characteristics), or Article 9 (sustainable investment objective). Applies ESA Joint Supervisory Authority guidance, ESMA Q&A, and EU Taxonomy Regulation (EU) 2020/852 disclosure requirements.
tier: premium
inputs: none
---

# Esg Sfdr Categorization

## Description
Classifies EU investment funds under SFDR (EU) 2019/2088 as Article 6 (no ESG), Article 8 (promotes ESG characteristics), or Article 9 (sustainable investment objective). Applies ESA Joint Supervisory Authority guidance, ESMA Q&A, and EU Taxonomy Regulation (EU) 2020/852 disclosure requirements. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "esg_sfdr_categorization",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "esg_sfdr_categorization"`.
