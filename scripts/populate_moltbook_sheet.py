#!/usr/bin/env python3
"""
One-time Google Sheet population script for the Moltbook Engagement command center.
Run by Claude Code (not Snowdrop) — uses Claude Code budget, not the $20 OpenRouter cap.

Usage:
  # With GOOGLE_SERVICE_ACCOUNT_JSON already in environment:
  python scripts/populate_moltbook_sheet.py

  # Or pass the HP .env path:
  DOTENV_PATH=~/.env python scripts/populate_moltbook_sheet.py

Sheet ID: 1dpOdvas07uS4sB80BAS_nG8eDNbHdgzpDsVdf6C-tbI
"""
import os
import sys
import json
from datetime import date, timedelta
from pathlib import Path

# ── Bootstrap: load .env ──────────────────────────────────────────────────────
_env_path = Path(os.environ.get("DOTENV_PATH", Path.home() / "snowdrop-core" / ".env"))
if _env_path.exists():
    with open(_env_path) as _f:
        for _line in _f:
            _line = _line.strip()
            if _line and not _line.startswith("#") and "=" in _line:
                _k, _, _v = _line.partition("=")
                os.environ.setdefault(_k.strip(), _v.strip())

import gspread

SHEET_ID = "1dpOdvas07uS4sB80BAS_nG8eDNbHdgzpDsVdf6C-tbI"

# ── Auth ──────────────────────────────────────────────────────────────────────
def get_client():
    sa_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON", "")
    if sa_json:
        return gspread.service_account_from_dict(json.loads(sa_json))
    creds_path = os.environ.get("GCP_SERVICE_ACCOUNT_FILE", "")
    if creds_path and Path(creds_path).exists():
        return gspread.service_account(filename=creds_path)
    raise ValueError("Set GOOGLE_SERVICE_ACCOUNT_JSON or GCP_SERVICE_ACCOUNT_FILE")


# ── Submolt data ───────────────────────────────────────────────────────────────
# Columns: Submolt, Members, Description, Overall, Finance, CapMarkets, Crypto/DeFi,
#          Agents/AI, MCP/Tools, Coding/Eng, Promotion/PR, Social, Strategy, Freq, Status
# Scoring 1-10 per dimension; Overall = headline relevance score
SUBMOLTS = [
    # Submolt, Members, Description, Overall, Finance, CapMarkets, Crypto, Agents, MCP, Coding, Promo, Social, Strategy, Freq, Status
    ("finance",             "?", "Financial topics and markets",                      10, 10, 8, 6, 5, 6, 4, 5, 3, "FINANCE_AUTH",  "4x/day", "active"),
    ("trading",             "?", "Trading strategies and market discussion",           10, 10, 7, 7, 4, 5, 4, 5, 3, "FINANCE_AUTH",  "4x/day", "active"),
    ("agentfinance",        "?", "Finance-focused AI agent discussion",               10, 9,  8, 6, 10, 9, 5, 8, 4, "AGENT_NATIVE",  "4x/day", "active"),
    ("agents",              "?", "General AI agent community",                         9, 5,  4, 5,  10, 8, 6, 8, 5, "AGENT_NATIVE",  "4x/day", "active"),
    ("mcp",                 "?", "Model Context Protocol community",                  10, 4,  3, 4,  8, 10, 7, 10, 5, "TOOL_PROMO",   "4x/day", "active"),
    ("agentskills",         "?", "AI agent skills and capabilities",                  10, 5,  3, 4,  9, 10, 6, 10, 5, "TOOL_PROMO",   "4x/day", "active"),
    ("aitools",             "?", "AI tools and utilities",                             9, 4,  3, 4,  7,  9, 6,  9, 4, "TOOL_PROMO",   "4x/day", "active"),
    ("tools",               "?", "General tools and utilities",                        8, 3,  2, 3,  6,  8, 6,  8, 3, "TOOL_PROMO",   "3x/day", "active"),
    ("crypto",              "?", "Cryptocurrency discussion",                          9, 7,  5, 10, 5,  6, 4,  7, 3, "CRYPTO_PITCH", "3x/day", "active"),
    ("defi",                "?", "Decentralized finance",                              9, 8,  6, 10, 5,  6, 4,  7, 3, "CRYPTO_PITCH", "3x/day", "active"),
    ("usdc",                "?", "USDC stablecoin community",                          8, 7,  4, 9,  4,  5, 3,  6, 2, "CRYPTO_PITCH", "2x/day", "active"),
    ("investing",           "?", "Investment strategies and discussion",               9, 9,  7, 5,  4,  5, 4,  5, 3, "FINANCE_AUTH",  "3x/day", "active"),
    ("economics",           "?", "Economic theory and current events",                 8, 7,  6, 4,  4,  4, 3,  4, 3, "FINANCE_AUTH",  "2x/day", "active"),
    ("algotrading",         "?", "Algorithmic and quantitative trading",               9, 9,  7, 6,  5,  6, 7,  6, 3, "FINANCE_AUTH",  "3x/day", "active"),
    ("quantmolt",           "?", "Quantitative finance and modeling",                  9, 9,  8, 5,  5,  6, 7,  5, 2, "FINANCE_AUTH",  "2x/day", "active"),
    ("agenteconomy",        "?", "Agent-driven economic systems",                      9, 7,  5, 6, 10,  8, 5,  9, 4, "AGENT_NATIVE",  "3x/day", "active"),
    ("agentcommerce",       "?", "Agent commerce and marketplace",                     8, 6,  4, 5,  9,  7, 5,  8, 4, "AGENT_NATIVE",  "3x/day", "active"),
    ("agenteconomics",      "?", "Economics of AI agent systems",                      8, 7,  5, 5,  9,  7, 5,  8, 3, "AGENT_NATIVE",  "2x/day", "active"),
    ("agent-economy",       "?", "Agent economy (variant community)",                  8, 6,  4, 5,  9,  7, 4,  8, 3, "AGENT_NATIVE",  "2x/day", "active"),
    ("aiagents",            "?", "AI agents (general)",                                9, 4,  3, 4, 10,  8, 6,  8, 4, "AGENT_NATIVE",  "3x/day", "active"),
    ("ai-agents",           "?", "AI agents (hyphenated variant)",                     9, 4,  3, 4, 10,  8, 6,  8, 4, "AGENT_NATIVE",  "3x/day", "active"),
    ("agentops",            "?", "Agent operations and infrastructure",                8, 4,  3, 4,  8,  8, 7,  8, 3, "DEV_RECRUIT",   "2x/day", "active"),
    ("agentinfrastructure", "?", "AI agent infrastructure",                            8, 4,  3, 4,  8,  9, 7,  8, 3, "DEV_RECRUIT",   "2x/day", "active"),
    ("agent-ops",           "?", "Agent ops (variant)",                                7, 3,  2, 3,  7,  7, 6,  7, 3, "DEV_RECRUIT",   "2x/day", "active"),
    ("sli-agents",          "?", "SLI/reliability for agents",                         7, 3,  2, 3,  7,  7, 7,  6, 3, "AGENT_NATIVE",  "1x/day", "active"),
    ("coding",              "?", "Programming and software development",               7, 2,  2, 3,  5,  6, 9,  5, 3, "DEV_RECRUIT",   "3x/day", "active"),
    ("dev",                 "?", "Developer discussion",                               7, 2,  2, 3,  5,  6, 9,  5, 3, "DEV_RECRUIT",   "3x/day", "active"),
    ("programming",         "?", "Programming languages and tools",                    7, 2,  2, 3,  5,  6, 9,  5, 3, "DEV_RECRUIT",   "3x/day", "active"),
    ("ai-coding",           "?", "AI-assisted coding",                                 8, 3,  2, 3,  7,  7, 9,  7, 3, "DEV_RECRUIT",   "3x/day", "active"),
    ("engineering",         "?", "Software engineering practice",                      7, 2,  2, 3,  5,  6, 9,  5, 3, "DEV_RECRUIT",   "2x/day", "active"),
    ("automation",          "?", "Automation tools and workflows",                     7, 3,  2, 4,  6,  7, 7,  6, 4, "DEV_RECRUIT",   "2x/day", "active"),
    ("optimization",        "?", "Performance and optimization",                       7, 4,  3, 4,  6,  7, 7,  7, 3, "TOOL_PROMO",    "2x/day", "active"),
    ("skills",              "?", "Skills and capabilities",                             9, 4,  3, 3,  8,  9, 6,  9, 4, "TOOL_PROMO",    "3x/day", "active"),
    ("tips",                "?", "Tips and tricks",                                    7, 3,  2, 3,  5,  7, 5,  7, 4, "TOOL_PROMO",    "2x/day", "active"),
    ("agenttips",           "?", "Tips specifically for AI agents",                    8, 4,  3, 4,  7,  8, 5,  8, 5, "TOOL_PROMO",    "3x/day", "active"),
    ("showandtell",         "?", "Show off projects and builds",                       8, 3,  2, 3,  6,  7, 5,  9, 5, "SOFT_SOCIAL",   "2x/day", "active"),
    ("creativeprojects",    "?", "Creative project showcase",                          6, 2,  1, 2,  4,  5, 4,  6, 5, "SOFT_SOCIAL",   "1x/day", "active"),
    ("todayilearned",       "?", "TIL posts — learning and discoveries",               7, 4,  3, 3,  5,  6, 4,  5, 6, "SOFT_SOCIAL",   "2x/day", "active"),
    ("offmychest",          "?", "Personal venting and reflections",                   5, 3,  2, 2,  4,  4, 3,  3, 7, "SOFT_SOCIAL",   "1x/day", "active"),
    ("productivity",        "?", "Productivity tools and workflows",                   6, 3,  2, 3,  5,  6, 5,  5, 5, "SOFT_SOCIAL",   "1x/day", "active"),
    ("research",            "?", "Research and academic discussion",                   7, 5,  4, 3,  5,  6, 5,  4, 4, "SOFT_SOCIAL",   "2x/day", "active"),
    ("nightshift",          "?", "Autonomous agents working while humans sleep",       6, 3,  2, 3,  6,  5, 4,  5, 6, "SOFT_SOCIAL",   "1x/day", "active"),
    ("technology",          "?", "General technology discussion",                      6, 3,  2, 3,  5,  5, 5,  4, 4, "SOFT_SOCIAL",   "1x/day", "active"),
    ("tech",                "?", "Tech (short form)",                                  5, 2,  2, 2,  4,  4, 4,  3, 4, "SOFT_SOCIAL",   "1x/day", "active"),
]

SUBMOLT_HEADERS = [
    "Submolt", "Members", "Description",
    "Overall", "Finance", "CapMarkets", "Crypto/DeFi", "Agents/AI",
    "MCP/Tools", "Coding/Eng", "Promotion/PR", "Social",
    "Strategy", "Freq", "Status"
]

# ── Weekly forecast ────────────────────────────────────────────────────────────
FORECAST_HEADERS = [
    "Week Start", "Week End", "Posts Target", "Posts Actual",
    "Engagement Target", "Engagement Actual", "Cumulative Target", "Notes"
]

def build_forecast_rows():
    """53 weeks starting Feb 22 2026."""
    rows = []
    start = date(2026, 2, 22)
    # Ramp: weeks 1-4 = 50/week, weeks 5-8 = 100/week, weeks 9-12 = 168/week, week 13+ = 240/week
    cumulative_target = 0
    for i in range(53):
        week_start = start + timedelta(weeks=i)
        week_end = week_start + timedelta(days=6)
        if i < 4:
            target = 50
        elif i < 8:
            target = 100
        elif i < 12:
            target = 168
        else:
            target = 240
        # Engagement target: ~15% of posts get 1+ upvote, ~5% get a comment
        eng_target = round(target * 0.15)
        cumulative_target += target
        rows.append([
            week_start.strftime("%Y-%m-%d"),
            week_end.strftime("%Y-%m-%d"),
            target,
            "",   # Posts Actual (Snowdrop fills)
            eng_target,
            "",   # Engagement Actual
            cumulative_target,
            "",   # Notes
        ])
    return rows


# ── Tab content ────────────────────────────────────────────────────────────────
POST_LOG_HEADERS = ["Date", "Time (UTC)", "Submolt", "Title", "Post ID", "Strategy", "Model", "Word Count", "URL"]
PERFORMANCE_HEADERS = ["Post ID", "Submolt", "Title", "Upvotes", "Comments", "Last Checked", "ROI Score", "Notes"]
SUBMOLT_PERF_HEADERS = ["Submolt", "Posts Made", "Total Upvotes", "Total Comments", "Avg Upvotes/Post", "Avg Comments/Post", "Best Post", "Last Posted", "ROI Grade"]
DAILY_HEADERS = ["Date", "Posts", "Upvotes", "Comments", "Best Post", "New Submolts", "Slack Sent", "Notes"]

INSTRUCTIONS_TEXT = """MOLTBOOK ENGAGEMENT SHEET — INSTRUCTIONS FOR SNOWDROP
======================================================

Executive Summary:
This Google Sheet is your command center for tracking, analyzing, and optimizing
Moltbook engagement. It tells you where to post, how past posts performed, and
whether the effort is building real traction.

HOW YOU USE THIS SHEET (CHEAP MODEL GUIDE)
-------------------------------------------

1. BEFORE POSTING (each daemon run):
   - Call moltbook_engagement_sheet(action="get_submolt_list")
   - This returns your active submolts with strategy types and scores
   - Your daemon's posting_queue handles rotation automatically

2. AFTER EACH POST:
   - Call moltbook_engagement_sheet(action="log_post", data={...})
   - Required: submolt, title, post_id, strategy, model, word_count, url
   - Takes ~1 second, costs nothing (no LLM needed)

3. DAILY SLACK REPORT (first run after midnight UTC):
   - Call moltbook_engagement_sheet(action="daily_report")
   - Returns a formatted summary string → pass to slack_post()
   - Also call moltbook_engagement_sheet(action="log_daily_report", data={...})

4. WEEKLY ACTUAL UPDATE (every Sunday or Monday):
   - Call moltbook_engagement_sheet(action="update_weekly_actual", data={posts_actual: N})
   - Fills in the WEEKLY FORECAST tab with real numbers

INTERPRETING ROI
----------------
- If a submolt has 0 upvotes after 20+ posts → downgrade its Freq to "pause"
- If a submolt averages 2+ upvotes/post → upgrade its Freq to "6x/day"
- If engagement is <5% of posts → experiment with different content types
- Traction signal: any post hitting 10+ upvotes in 24h is a winner; post more like it

STRATEGY TYPES
--------------
FINANCE_AUTH  → financial_content_draft() with authoritative tone
AGENT_NATIVE  → compose_message() as agent-to-agent, pitch Watering Hole
TOOL_PROMO    → compose_message() promoting MCP skills, free trial
DEV_RECRUIT   → compose_message() showcasing open source, asking for contributors
CRYPTO_PITCH  → financial_content_draft() on DeFi/TON/stablecoins
SOFT_SOCIAL   → compose_message() in personal voice, light plugs

FORECAST TARGETS
----------------
Week 1-4:  50 posts/week (ramping up)
Week 5-8:  100 posts/week
Week 9-12: 168 posts/week
Week 13+:  240 posts/week (steady state = 4 posts/run × 48 runs/day × 7 days... but really ~4×30min×24h = 192/day)
Year total target: ~10,000 posts

ESCALATION SIGNAL TO THUNDER
------------------------------
If OpenRouter balance drops below $10, send Slack alert immediately.
If Moltbook returns 429 errors on 3+ consecutive runs, alert Thunder.
If cumulative posts are >20% below weekly target, alert Thunder.
"""


def get_or_create_worksheet(sheet, title: str, rows: int = 1000, cols: int = 20):
    try:
        return sheet.worksheet(title)
    except gspread.WorksheetNotFound:
        return sheet.add_worksheet(title=title, rows=rows, cols=cols)


def populate_tab(ws, headers: list, data_rows: list = None, clear: bool = True):
    if clear:
        ws.clear()
    all_rows = [headers]
    if data_rows:
        all_rows.extend(data_rows)
    ws.update(all_rows, value_input_option="USER_ENTERED")
    # Bold the header row
    ws.format("1:1", {"textFormat": {"bold": True}})
    print(f"  ✓ {ws.title}: {len(all_rows)-1} data rows + header")


def main():
    print("Connecting to Google Sheets...")
    gc = get_client()
    sheet = gc.open_by_key(SHEET_ID)
    print(f"Opened: {sheet.title}")

    # 1. SUBMOLT DIRECTORY
    print("\nPopulating SUBMOLT DIRECTORY...")
    ws = get_or_create_worksheet(sheet, "SUBMOLT DIRECTORY")
    submolt_rows = [list(s) for s in SUBMOLTS]
    populate_tab(ws, SUBMOLT_HEADERS, submolt_rows)

    # 2. POST LOG (headers only)
    print("Setting up POST LOG...")
    ws = get_or_create_worksheet(sheet, "POST LOG")
    populate_tab(ws, POST_LOG_HEADERS, [])

    # 3. POST PERFORMANCE (headers only)
    print("Setting up POST PERFORMANCE...")
    ws = get_or_create_worksheet(sheet, "POST PERFORMANCE")
    populate_tab(ws, PERFORMANCE_HEADERS, [])

    # 4. SUBMOLT PERFORMANCE (seed with submolt names)
    print("Seeding SUBMOLT PERFORMANCE...")
    ws = get_or_create_worksheet(sheet, "SUBMOLT PERFORMANCE")
    seed_rows = [[s[0], 0, 0, 0, 0, 0, "", "", "—"] for s in SUBMOLTS]
    populate_tab(ws, SUBMOLT_PERF_HEADERS, seed_rows)

    # 5. WEEKLY FORECAST
    print("Generating WEEKLY FORECAST (53 weeks)...")
    ws = get_or_create_worksheet(sheet, "WEEKLY FORECAST")
    forecast_rows = build_forecast_rows()
    populate_tab(ws, FORECAST_HEADERS, forecast_rows)

    # 6. DAILY REPORTS (headers only)
    print("Setting up DAILY REPORTS...")
    ws = get_or_create_worksheet(sheet, "DAILY REPORTS")
    populate_tab(ws, DAILY_HEADERS, [])

    # 7. INSTRUCTIONS
    print("Writing INSTRUCTIONS...")
    ws = get_or_create_worksheet(sheet, "INSTRUCTIONS")
    ws.clear()
    # Write the instructions as a single cell blob (column A, row 1)
    lines = INSTRUCTIONS_TEXT.strip().split("\n")
    ws.update([[line] for line in lines])
    print(f"  ✓ INSTRUCTIONS: {len(lines)} lines")

    print("\n✅ Sheet fully populated!")
    print(f"   https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit")


if __name__ == "__main__":
    main()
