---
skill: tax_deferred_accounts_guide
category: education
description: Returns educational content on tax-advantaged accounts: 401(k), IRA, Roth, HSA, contribution limits, and RMDs.
tier: free
inputs: none
---

# Tax Deferred Accounts Guide

## Description
Returns educational content on tax-advantaged accounts: 401(k), IRA, Roth, HSA, contribution limits, and RMDs.

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
  "tool": "tax_deferred_accounts_guide",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "tax_deferred_accounts_guide"`.
