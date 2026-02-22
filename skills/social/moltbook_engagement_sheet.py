"""
Moltbook Engagement Google Sheet skill — Snowdrop's command center for tracking
which submolts she's posting to, how those posts perform, and whether the
engagement effort is generating real traction.

Sheet ID: 1dpOdvas07uS4sB80BAS_nG8eDNbHdgzpDsVdf6C-tbI
Auth: GOOGLE_SERVICE_ACCOUNT_JSON (full service account JSON as env var string)

Tabs:
  POST LOG           — every post made, appended in real-time
  POST PERFORMANCE   — upvotes + comments per post (polled periodically)
  SUBMOLT DIRECTORY  — all submolts with rankings and recommended strategy
  SUBMOLT PERFORMANCE — aggregate stats per submolt
  WEEKLY FORECAST    — Feb 2026 - Feb 2027 weekly targets vs actuals
  DAILY REPORTS      — one row per day for trend analysis
  INSTRUCTIONS       — how to use this sheet with a cheap model
"""
import os
import json
import time
from datetime import datetime, timezone, date, timedelta

TOOL_META = {
    "name": "moltbook_engagement_sheet",
    "description": (
        "Read and write the Moltbook Engagement Google Sheet — Snowdrop's command center. "
        "Actions: 'log_post' (append post to POST LOG), 'get_submolt_list' (read SUBMOLT DIRECTORY "
        "for strategy routing), 'get_stats' (aggregate performance data), 'daily_report' (compile "
        "daily stats from POST LOG, suitable for Slack), 'update_weekly_actual' (fill in this "
        "week's actual post count in WEEKLY FORECAST), 'update_performance' (upsert post upvotes/"
        "comments into POST PERFORMANCE tab — called by the performance poller), 'update_submolt_perf' "
        "(upsert per-submolt aggregate stats into SUBMOLT PERFORMANCE tab — called by the poller). "
        "Designed to run cheaply with Gemini Flash Lite."
    ),
}

SHEET_ID = "1dpOdvas07uS4sB80BAS_nG8eDNbHdgzpDsVdf6C-tbI"

# Tab names
TAB_POST_LOG = "POST LOG"
TAB_PERFORMANCE = "POST PERFORMANCE"
TAB_SUBMOLTS = "SUBMOLT DIRECTORY"
TAB_SUBMOLT_PERF = "SUBMOLT PERFORMANCE"
TAB_FORECAST = "WEEKLY FORECAST"
TAB_DAILY = "DAILY REPORTS"
TAB_INSTRUCTIONS = "INSTRUCTIONS"


def _get_client():
    """Return authenticated gspread client. Supports JSON string or file path."""
    import gspread
    sa_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON", "")
    if sa_json and sa_json.strip().startswith("{"):
        # Env var contains actual JSON content
        creds_dict = json.loads(sa_json)
        return gspread.service_account_from_dict(creds_dict)
    if sa_json and os.path.exists(sa_json):
        # Env var is a file path
        return gspread.service_account(filename=sa_json)
    # Fallback: GCP_SERVICE_ACCOUNT_FILE
    creds_path = os.environ.get("GCP_SERVICE_ACCOUNT_FILE", "")
    if creds_path and os.path.exists(creds_path):
        return gspread.service_account(filename=creds_path)
    raise ValueError("No Google service account credentials found (GOOGLE_SERVICE_ACCOUNT_JSON or GCP_SERVICE_ACCOUNT_FILE)")


def moltbook_engagement_sheet(action: str, data: dict = None) -> dict:
    """
    Interact with the Moltbook Engagement Google Sheet.

    Args:
        action: One of 'log_post' | 'get_submolt_list' | 'get_stats' |
                'daily_report' | 'update_weekly_actual' | 'log_daily_report'
        data: Payload dict, required for write actions:
              log_post: {submolt, title, post_id, model, word_count, url, strategy}
              update_weekly_actual: {posts_actual, engagement_actual}
              log_daily_report: {posts, upvotes, comments, best_post, slack_sent}
    """
    ts = datetime.now(timezone.utc).isoformat()
    data = data or {}

    try:
        gc = _get_client()
        sheet = gc.open_by_key(SHEET_ID)

        if action == "log_post":
            return _log_post(sheet, data, ts)
        elif action == "get_submolt_list":
            return _get_submolt_list(sheet, ts)
        elif action == "get_stats":
            return _get_stats(sheet, ts)
        elif action == "daily_report":
            return _daily_report(sheet, ts)
        elif action == "update_weekly_actual":
            return _update_weekly_actual(sheet, data, ts)
        elif action == "log_daily_report":
            return _log_daily_report(sheet, data, ts)
        elif action == "update_performance":
            return _update_performance(sheet, data, ts)
        elif action == "update_submolt_perf":
            return _update_submolt_perf(sheet, data, ts)
        else:
            return {
                "status": "error",
                "data": {"message": f"Unknown action: {action}"},
                "timestamp": ts,
            }
    except Exception as e:
        return {
            "status": "error",
            "data": {"message": str(e)},
            "timestamp": ts,
        }


def _log_post(sheet, data: dict, ts: str) -> dict:
    """Append a row to POST LOG."""
    ws = sheet.worksheet(TAB_POST_LOG)
    today = datetime.now(timezone.utc)
    row = [
        today.strftime("%Y-%m-%d"),
        today.strftime("%H:%M UTC"),
        data.get("submolt", ""),
        data.get("title", "")[:100],
        data.get("post_id", ""),
        data.get("strategy", ""),
        data.get("model", ""),
        data.get("word_count", ""),
        data.get("url", ""),
    ]
    ws.append_row(row, value_input_option="USER_ENTERED")
    return {
        "status": "ok",
        "data": {"logged": True, "submolt": data.get("submolt"), "post_id": data.get("post_id")},
        "timestamp": ts,
    }


def _get_submolt_list(sheet, ts: str) -> dict:
    """Read SUBMOLT DIRECTORY and return structured list for daemon routing."""
    ws = sheet.worksheet(TAB_SUBMOLTS)
    rows = ws.get_all_records()
    submolts = []
    for r in rows:
        name = r.get("Submolt", "")
        if not name:
            continue
        submolts.append({
            "name": name,
            "strategy": r.get("Strategy", "FINANCE_AUTH"),
            "overall_score": r.get("Overall", 5),
            "status": r.get("Status", "active"),
            "recommended_freq": r.get("Freq", "daily"),
        })
    return {
        "status": "ok",
        "data": {"submolts": submolts, "count": len(submolts)},
        "timestamp": ts,
    }


def _get_stats(sheet, ts: str) -> dict:
    """Read SUBMOLT PERFORMANCE for aggregate stats."""
    try:
        ws = sheet.worksheet(TAB_SUBMOLT_PERF)
        rows = ws.get_all_records()
        return {
            "status": "ok",
            "data": {"submolt_stats": rows, "count": len(rows)},
            "timestamp": ts,
        }
    except Exception as e:
        return {
            "status": "ok",
            "data": {"submolt_stats": [], "count": 0, "note": str(e)},
            "timestamp": ts,
        }


def _daily_report(sheet, ts: str) -> dict:
    """Compile today's stats from POST LOG for a Slack report."""
    ws = sheet.worksheet(TAB_POST_LOG)
    rows = ws.get_all_records()
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    today_rows = [r for r in rows if r.get("Date", "") == today]
    posts = len(today_rows)
    submolts_hit = list(set(r.get("Submolt", "") for r in today_rows if r.get("Submolt")))
    strategies_used = list(set(r.get("Strategy", "") for r in today_rows if r.get("Strategy")))

    if posts == 0:
        summary = f"*Snowdrop Daily Report — {today}*\nNo posts made today yet. Daemon running, checking for opportunities."
    else:
        submolt_list = ", ".join(f"m/{s}" for s in submolts_hit[:8])
        summary = (
            f"*Snowdrop Daily Report — {today}*\n"
            f"• Posts made: {posts}\n"
            f"• Submolts covered: {submolt_list}\n"
            f"• Strategies used: {', '.join(strategies_used)}\n"
            f"• Models: {', '.join(set(r.get('Model','') for r in today_rows if r.get('Model')))}"
        )

    return {
        "status": "ok",
        "data": {
            "summary": summary,
            "posts_today": posts,
            "submolts_hit": submolts_hit,
            "date": today,
        },
        "timestamp": ts,
    }


def _update_weekly_actual(sheet, data: dict, ts: str) -> dict:
    """Find this week's row in WEEKLY FORECAST and fill in actuals."""
    ws = sheet.worksheet(TAB_FORECAST)
    rows = ws.get_all_values()
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # Find the week row where Week Start <= today <= Week End
    target_row = None
    for i, row in enumerate(rows[1:], start=2):  # skip header
        if len(row) >= 2 and row[0] <= today <= row[1]:
            target_row = i
            break

    if not target_row:
        return {
            "status": "error",
            "data": {"message": f"No forecast row found for date {today}"},
            "timestamp": ts,
        }

    # Posts Actual = col D (index 4), Engagement Actual = col F (index 6)
    posts_actual = data.get("posts_actual", "")
    engagement_actual = data.get("engagement_actual", "")
    ws.update_cell(target_row, 4, posts_actual)
    if engagement_actual:
        ws.update_cell(target_row, 6, engagement_actual)

    return {
        "status": "ok",
        "data": {"week_row": target_row, "posts_actual": posts_actual},
        "timestamp": ts,
    }


def _log_daily_report(sheet, data: dict, ts: str) -> dict:
    """Append a row to DAILY REPORTS tab."""
    ws = sheet.worksheet(TAB_DAILY)
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    row = [
        today,
        data.get("posts", 0),
        data.get("upvotes", 0),
        data.get("comments", 0),
        data.get("best_post", ""),
        data.get("new_submolts", 0),
        "Yes" if data.get("slack_sent") else "No",
        data.get("notes", ""),
    ]
    ws.append_row(row, value_input_option="USER_ENTERED")
    return {
        "status": "ok",
        "data": {"logged": True, "date": today},
        "timestamp": ts,
    }


def _update_performance(sheet, data: dict, ts: str) -> dict:
    """Upsert a post's upvotes/comments into POST PERFORMANCE tab.

    data keys: post_id, submolt, title, upvotes, comments, roi_score, date_polled
    POST PERFORMANCE columns: A=Post ID, B=Submolt, C=Title, D=Upvotes, E=Comments, F=ROI Score, G=Date Polled
    """
    ws = sheet.worksheet(TAB_PERFORMANCE)
    all_values = ws.get_all_values()

    post_id = str(data.get("post_id", ""))
    new_row = [
        post_id,
        data.get("submolt", ""),
        (data.get("title", "") or "")[:100],
        data.get("upvotes", 0),
        data.get("comments", 0),
        data.get("roi_score", 0),
        data.get("date_polled", datetime.now(timezone.utc).strftime("%Y-%m-%d")),
    ]

    # Find existing row by post_id (col A = index 0), skip header row
    target_row = None
    for i, row in enumerate(all_values[1:], start=2):
        if row and str(row[0]) == post_id:
            target_row = i
            break

    if target_row:
        # Update in place (columns A-G = 1-7)
        ws.update(f"A{target_row}:G{target_row}", [new_row])
    else:
        ws.append_row(new_row, value_input_option="USER_ENTERED")

    return {
        "status": "ok",
        "data": {
            "upserted": True,
            "post_id": post_id,
            "action": "updated" if target_row else "appended",
        },
        "timestamp": ts,
    }


def _update_submolt_perf(sheet, data: dict, ts: str) -> dict:
    """Upsert per-submolt aggregate stats into SUBMOLT PERFORMANCE tab.

    data keys: submolt, posts_made, total_upvotes, total_comments,
               avg_upvotes, avg_comments, best_post, roi_grade
    SUBMOLT PERFORMANCE columns: A=Submolt, B=Posts Made, C=Total Upvotes,
                                  D=Total Comments, E=Avg Upvotes, F=Avg Comments,
                                  G=Best Post, H=ROI Grade, I=Last Updated
    """
    ws = sheet.worksheet(TAB_SUBMOLT_PERF)
    all_values = ws.get_all_values()

    submolt = str(data.get("submolt", ""))
    new_row = [
        submolt,
        data.get("posts_made", 0),
        data.get("total_upvotes", 0),
        data.get("total_comments", 0),
        round(float(data.get("avg_upvotes", 0)), 2),
        round(float(data.get("avg_comments", 0)), 2),
        data.get("best_post", ""),
        data.get("roi_grade", "F"),
        datetime.now(timezone.utc).strftime("%Y-%m-%d"),
    ]

    target_row = None
    for i, row in enumerate(all_values[1:], start=2):
        if row and str(row[0]).lower() == submolt.lower():
            target_row = i
            break

    if target_row:
        ws.update(f"A{target_row}:I{target_row}", [new_row])
    else:
        ws.append_row(new_row, value_input_option="USER_ENTERED")

    return {
        "status": "ok",
        "data": {
            "upserted": True,
            "submolt": submolt,
            "roi_grade": data.get("roi_grade", "F"),
            "action": "updated" if target_row else "appended",
        },
        "timestamp": ts,
    }
