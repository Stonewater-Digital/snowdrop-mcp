---
title: Empty-Params SKILL.md Report
generated: 2026-05-06
author: Snowdrop Quality Agent
---

# Empty-Params SKILL.md Report

## Executive Summary

This report documents the audit of SKILL.md files with `_No parameters defined._` in their Parameters section. The audit was run as part of the quality follow-up on 2026-05-06. The generator (`scripts/generate_skill_docs.py`) was enhanced to extract parameters from Python function AST signatures as a fallback, reducing empty-param files from 419 to 344.

## Table of Contents

1. [Summary Statistics](#summary-statistics)
2. [Category Breakdown](#category-breakdown)
3. [Why Premium Stubs Have No Params](#why-premium-stubs-have-no-params)
4. [Remaining Free Skills with No Params](#remaining-free-skills-with-no-params)
5. [Fix Applied](#fix-applied)
6. [Recommendation](#recommendation)

---

## Summary Statistics

| Metric | Count |
|--------|-------|
| Total SKILL.md files | 1,949 |
| Empty-param files **before** this fix | 419 |
| Empty-param files **after** this fix | 344 |
| Fixed by AST signature extraction | 75 |
| Remaining: premium stubs (expected) | 298 |
| Remaining: zero-param free tools (expected) | 46 |

---

## Category Breakdown

The majority of remaining empty-param files are in premium-tier skill directories:

| Directory | Count | Reason |
|-----------|-------|--------|
| `skills/crypto_rwa/` | ~122 | Premium stubs with `paywall_response()` |
| `skills/fund_tax/` | ~100 | Premium stubs with `paywall_response()` |
| `skills/education/` | ~27 | Premium stubs |
| `skills/structured_products/` | ~25 | Premium stubs |
| `skills/public_data/` | ~15 | Legitimately zero-arg fetchers (e.g. `gold_price_fetcher()`) |
| Other free (zero-arg) | ~31 | Legitimately parameterless tools |

---

## Why Premium Stubs Have No Params

Premium stubs are skills whose implementation is gated behind a paywall. Their Python
function bodies call `paywall_response()` immediately and do not expose any user-visible
parameters in the MCP interface. The TOOL_META deliberately omits `inputSchema` because:

1. **No user input is processed** — the stub returns a paywall message regardless of args.
2. **Exposing fake params would be misleading** — users/agents would pass values that are ignored.
3. **The paywall response is the interface** — tier upgrades unlock the real implementation.

These are **correctly documented** as having no parameters.

---

## Remaining Free Skills with No Params

The ~46 remaining free skills with `_No parameters defined._` are genuinely zero-argument
functions. Examples:

- `gold_price_fetcher()` — fetches current gold price from a fixed public API
- `vix_level_fetcher()` — fetches current VIX index level
- `yield_curve_fetcher()` — fetches current US Treasury yield curve
- `get_ab_test_insights()` — returns aggregated A/B test results

These zero-arg tools call external APIs or aggregate internal state without requiring user
input. Their empty params table is **accurate**.

---

## Fix Applied

`scripts/generate_skill_docs.py` was enhanced with a new function
`_extract_params_from_function_ast()` that:

1. Parses the skill `.py` file with Python's `ast` module
2. Finds the public skill function matching `TOOL_META["name"]`
3. Extracts argument names, type annotations, and default values
4. Maps Python type annotations to JSON Schema-like types (`str→string`, `int→integer`, etc.)
5. Marks args without defaults as `required=True`

This fallback is only triggered when:
- `TOOL_META` lacks both `inputSchema` and `parameters`
- The skill file does not contain `paywall_response` or `PREMIUM` markers

---

## Recommendation

Add a `--tier=free` filter to `scripts/generate_skill_docs.py` so that premium stubs can
be explicitly skipped during bulk regeneration runs. This would make the generator's
behavior explicit rather than relying on content-based heuristics.

Tracking issue: see the GitHub issue linked from this PR for ongoing work on remaining
empties.
