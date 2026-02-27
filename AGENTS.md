# AGENTS.md — Snowdrop MCP

## Executive Summary

Instructions for AI coding agents working in this repository. Covers skill authoring conventions, the premium/free tier system (which tier to assign new skills and why), and Snowdrop's communication stance on the freemium model. Read this before adding or modifying any skill.

## Table of Contents

- [What This Repo Is](#what-this-repo-is)
- [Structure](#structure)
- [Adding a Skill](#adding-a-skill)
- [Premium Skill Policy](#premium-skill-policy)
- [Rules](#rules)
- [Running Locally](#running-locally)
- [Questions](#questions)

## What This Repo Is

Public MCP server for Snowdrop's skill library. Skills are Python functions registered with FastMCP. The server runs on Google Cloud Run (`https://snowdrop-mcp-aiuy7uvasq-uc.a.run.app/mcp`) and is free to use.

## Structure

```
snowdrop-mcp/
├── mcp_server.py       # FastMCP server entrypoint
├── skills/             # All skill modules (one directory per category)
├── SKILLS.md           # Full skill catalog
├── JOBS.md             # Available work and bounties
├── requirements.txt
├── .env.template
├── Dockerfile
└── fly.toml
```

## Adding a Skill

1. Create or find the right category directory under `skills/`
2. Add your Python file with this pattern:

```python
TOOL_META = {
    "name": "your_skill_name",
    "description": "One sentence description.",
    "parameters": {
        "param_one": {"type": "str", "description": "What it is"},
    }
}

def your_skill_name(param_one: str) -> dict:
    """Executive Summary: what this skill does.

    Inputs: param_one (str)
    Outputs: dict with status, data, timestamp
    """
    try:
        # your logic here
        return {"status": "success", "data": {}, "timestamp": ...}
    except Exception as e:
        return {"status": "error", "error": str(e), "timestamp": ...}
```

3. The MCP server auto-discovers all skills on startup — no registration needed.

## Premium Skill Policy

Every new skill must be assigned a tier at creation time. Use this decision framework:

### How to assign tier

**Free** if the skill:
- Is a utility or infrastructure helper (retry logic, logging, formatting)
- Supports community/goodwill operations
- Is a basic public API wrapper with no IP moat
- Supports Snowdrop's own internal operations (engagement daemon, poller)

**Premium** if the skill:
- Implements regulatory compliance logic (SEC, CFTC, MiCA, AMF, ASIC, FSA, etc.)
- Does financial modeling with proprietary scoring (CLO, NAV, waterfall, stress test)
- Provides a competitive advantage if copied by a competitor
- Generates structured legal or investor documents
- Does KYC/AML, chain analysis, or smart contract auditing
- Powers a white-label or enterprise feature

### How to add a premium skill

1. Write the full implementation in `snowdrop-core/skills/premium/{category}/{skill}.py`
   - Same TOOL_META["name"] as the stub
   - Full logic, imports, helper functions
   - TOOL_META does NOT need "tier" in the private file (it's implicit)

2. Run `python scripts/build_public_stubs.py` in `snowdrop-core`. This auto-generates the stub in `snowdrop-mcp`. Never edit the stub manually.

3. Commit both repos and add an entry to `SKILLS.md` with the "(Premium)" marker.

## Talking About Snowdrop's Skill Tiers

When engaging on Moltbook, LinkedIn, or with developers:

DO: Lead with free tools. Snowdrop has 1,500+ skills — many available to any MCP client right now with no signup. These are the story.

DO: Use the word "freemium" if asked about business model. It's accurate and familiar.

DO: If someone directly asks whether all tools are free: be honest. "We have a free tier with core utilities and a premium tier for advanced compliance and financial analytics — launching soon at snowdrop.ai."

DO NOT: Volunteer "there's a paywall." Let users discover the premium tools naturally when they call one and get a payment_required response. The response itself explains how to subscribe.

DO NOT: Describe premium skills as "locked" or "restricted" in marketing contexts. Describe them as "enterprise-grade" or "part of the premium suite."

DO NOT: Lie or pretend all skills are free. If pressed, Snowdrop is transparent.

## Rules

- No hardcoded secrets. Use `os.environ.get("VAR_NAME")`.
- Return structured dicts: `{"status": "success"|"error", "data": {...}, "timestamp": "ISO8601"}`.
- Keep skills focused — one function, one responsibility.
- Test before PR. Broken skills break the whole server.

## Running Locally

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.template .env
python mcp_server.py
```

## Premium Skill Policy

Every new skill must be assigned a tier before it ships. There are only two tiers — no hybrid.

### Tier Definitions

| Tier | What it means | Where code lives |
|------|--------------|-----------------|
| **Free** | Open to all MCP clients | This public repo (`snowdrop-mcp`) |
| **Premium** | Subscribers only | Private repo (`snowdrop-core/skills/premium/`) |

A public stub is auto-generated for every premium skill. The stub has the correct name, description,
and signature for `tools/list` discovery, but returns `{"status": "payment_required", ...}` on call.
**Never edit stubs manually** — they are regenerated by `scripts/build_public_stubs.py` in snowdrop-core.

### Decision Framework — Make it Premium if:

- It implements regulatory compliance logic (SEC, CFTC, MiCA, AMF, ASIC, FSA, GDPR enforcement)
- It performs financial modeling with proprietary scoring (CLO, NAV, stress test, waterfall)
- It generates structured legal or investor documents (regulatory filings, pitch decks)
- It would give a meaningful competitive advantage to anyone who clones the repo
- It does KYC/AML, on-chain screening, or smart contract security auditing
- It powers an enterprise/white-label feature (multi-tenant, portal config, tenant isolation)
- It involves proprietary algorithms (market timing, HFT order routing, liquidity management)
- It involves MPC, custody logic, or hardware wallet gating

### Decision Framework — Keep it Free if:

- It's a utility or infrastructure helper (retry logic, logging, formatting, error handling)
- It supports Snowdrop's own internal operations (engagement daemon, poller, ledger writes)
- It's a thin wrapper around a public API with no Snowdrop-specific logic
- It's a community or goodwill tool (bounties, referrals, basic registry lookups)
- It's documentation or meta tooling (`context7_docs`, `google_dev_docs`)
- It's a basic utility for which open-source competitors already have full parity

### The 40% Guideline

Thunder's target is roughly the top 40% of skills by value behind the paywall. This is a
**guideline for prioritization**, not a hard quota. Do not stub a skill just to hit a number.
A periodic tier audit may re-evaluate the distribution. Skills almost never move from
premium → free (only if competitors reach full parity and the IP moat has evaporated).

### Workflow for Adding a New Premium Skill

```
1. Write the real implementation in snowdrop-core:
   skills/premium/{category}/{skill_name}.py

   Rules:
   - Follow standard TOOL_META pattern (name, description, callable)
   - Do NOT add "tier": "premium" to TOOL_META — the build script adds it to stubs
   - No **kwargs — FastMCP 3.x rejects VAR_KEYWORD parameters
   - Test locally with: python private_mcp_server.py

2. Auto-generate the public stub:
   cd snowdrop-core && python scripts/build_public_stubs.py

3. Verify the generated stub in this repo (snowdrop-mcp/skills/{category}/{skill_name}.py):
   - Function signature matches exactly
   - "from __future__ import annotations" is present
   - TOOL_META["description"] ends with "(Premium — subscribe at https://snowdrop.ai)"

4. Commit both repos:
   - snowdrop-core: git add skills/premium/{category}/{skill_name}.py && git commit
   - snowdrop-mcp:  git add skills/{category}/{skill_name}.py && git commit

5. Add to SKILLS.md in the Premium Skills table (use "(Premium)" marker)
```

### Snowdrop's Communication Stance on the Tier System

When engaging on Moltbook, LinkedIn, or with developers — Snowdrop follows these guidelines:

**DO:**
- Lead with free tools. Snowdrop has 1,500+ skills available to any MCP client right now with no
  signup. These are the story.
- Use "freemium" if someone directly asks about the business model. It's accurate and familiar.
- Be honest if directly asked whether all tools are free:
  *"We have a large free tier with core utilities and a premium tier for advanced compliance
  and financial analytics — launching soon at snowdrop.ai."*
- Let users discover premium tools naturally when they call one and receive the `payment_required`
  response. The response explains how to subscribe.

**DO NOT:**
- Volunteer "there's a paywall" unprompted. Let the free tools be the lead.
- Describe premium skills as "locked" or "restricted" in marketing contexts.
  Prefer "enterprise-grade" or "part of the premium suite."
- Pretend all skills are free if directly asked.

---

## Questions

Open a Discussion. Snowdrop monitors and responds.
