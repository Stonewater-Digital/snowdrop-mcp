#!/usr/bin/env python3
"""
Add DASHBOARD tab to the Moltbook Engagement Google Sheet.

One-time setup script. Run on HP Spectre (snowdrop-node) or locally with
GOOGLE_SERVICE_ACCOUNT_JSON set in .env.

The DASHBOARD tab uses Google Sheets formulas that auto-update from:
  - POST LOG          → posts counts, strategy distribution
  - POST PERFORMANCE  → upvotes/comments (populated by performance poller)
  - WEEKLY FORECAST   → targets vs actuals
  - SUBMOLT PERFORMANCE → top submolts ranking

Run:
    python scripts/add_dashboard_tab.py
"""
import json
import os
import sys
from pathlib import Path

# Load .env
env_file = Path(__file__).parent.parent / ".env"
if env_file.exists():
    for line in env_file.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, _, v = line.partition("=")
            os.environ.setdefault(k.strip(), v.strip())

import gspread
from gspread.utils import rowcol_to_a1

SHEET_ID = "1dpOdvas07uS4sB80BAS_nG8eDNbHdgzpDsVdf6C-tbI"
DASHBOARD_TAB = "DASHBOARD"


def get_client():
    sa_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON", "")
    if sa_json and sa_json.strip().startswith("{"):
        return gspread.service_account_from_dict(json.loads(sa_json))
    if sa_json and os.path.exists(sa_json):
        return gspread.service_account(filename=sa_json)
    creds_path = os.environ.get("GCP_SERVICE_ACCOUNT_FILE", "")
    if creds_path and os.path.exists(creds_path):
        return gspread.service_account(filename=creds_path)
    raise ValueError("No Google service account credentials found")


def main():
    print("Connecting to Google Sheets...")
    gc = get_client()
    wb = gc.open_by_key(SHEET_ID)

    # Delete existing DASHBOARD tab if it exists
    existing_tabs = [ws.title for ws in wb.worksheets()]
    if DASHBOARD_TAB in existing_tabs:
        print(f"Removing existing {DASHBOARD_TAB} tab...")
        wb.del_worksheet(wb.worksheet(DASHBOARD_TAB))

    # Add DASHBOARD as the FIRST sheet (index=0)
    print("Creating DASHBOARD tab...")
    ws = wb.add_worksheet(title=DASHBOARD_TAB, rows=60, cols=4, index=0)

    # ── Build all cells in one batch_update call ──────────────────────────────
    # Format: (row, col, value)
    cells_data = [
        # Header
        (1, 1, "SNOWDROP MOLTBOOK INTELLIGENCE DASHBOARD"),
        (1, 2, '=TEXT(NOW(),"YYYY-MM-DD HH:MM") & " UTC"'),

        # TODAY section
        (3, 1, "── TODAY ──"),
        (4, 1, "Posts Today"),
        (4, 2, '=COUNTIF(\'POST LOG\'!A:A,TEXT(TODAY(),"YYYY-MM-DD"))'),
        (5, 1, "Submolts Hit Today"),
        (5, 2, '=IFERROR(COUNTA(UNIQUE(FILTER(\'POST LOG\'!C:C,\'POST LOG\'!A:A=TEXT(TODAY(),"YYYY-MM-DD")))),0)'),
        (6, 1, "Upvotes Today"),
        (6, 2, '=IFERROR(SUMPRODUCT((\'POST PERFORMANCE\'!G:G=TEXT(TODAY(),"YYYY-MM-DD"))*(\'POST PERFORMANCE\'!D:D)),0)'),
        (7, 1, "Comments Today"),
        (7, 2, '=IFERROR(SUMPRODUCT((\'POST PERFORMANCE\'!G:G=TEXT(TODAY(),"YYYY-MM-DD"))*(\'POST PERFORMANCE\'!E:E)),0)'),

        # THIS WEEK section
        (9, 1, "── THIS WEEK ──"),
        (10, 1, "Week Start"),
        (10, 2, "=TODAY()-WEEKDAY(TODAY(),2)+1"),
        (11, 1, "Posts This Week"),
        (11, 2, '=COUNTIFS(\'POST LOG\'!A:A,">="&TEXT(B10,"YYYY-MM-DD"))'),
        (12, 1, "Weekly Target"),
        (12, 2, '=IFERROR(VLOOKUP(TEXT(B10,"YYYY-MM-DD"),\'WEEKLY FORECAST\'!A:C,3,0),240)'),
        (13, 1, "% of Target"),
        (13, 2, "=IFERROR(B11/B12,0)"),
        (14, 1, "On Track?"),
        (14, 2, '=IF(B13>=0.7,"✅ On Track",IF(B13>=0.4,"⚠️ Behind","🔴 At Risk"))'),

        # ALL TIME section
        (16, 1, "── ALL TIME ──"),
        (17, 1, "Total Posts Made"),
        (17, 2, "=COUNTA('POST LOG'!E2:E10000)"),
        (18, 1, "Total Upvotes"),
        (18, 2, "=SUM('POST PERFORMANCE'!D:D)"),
        (19, 1, "Total Comments"),
        (19, 2, "=SUM('POST PERFORMANCE'!E:E)"),
        (20, 1, "Engagement Rate"),
        (20, 2, '=IFERROR(COUNTIF(\'POST PERFORMANCE\'!D:D,">0")/B17,0)'),
        (21, 1, "Avg Upvotes / Post"),
        (21, 2, "=IFERROR(B18/B17,0)"),
        (22, 1, "Avg Comments / Post"),
        (22, 2, "=IFERROR(B19/B17,0)"),
        (23, 1, "Est. Token Cost"),
        (23, 2, "=B17*0.0002"),
        (23, 3, "($0.0002/post — Gemini Flash Lite)"),

        # STRATEGY DISTRIBUTION section
        (25, 1, "── STRATEGY DISTRIBUTION ──"),
        (25, 2, "Posts"),
        (25, 3, "% of Total"),
        (26, 1, "FINANCE_AUTH"),
        (26, 2, "=COUNTIF('POST LOG'!F:F,\"FINANCE_AUTH\")"),
        (26, 3, "=IFERROR(B26/B17,0)"),
        (27, 1, "AGENT_NATIVE"),
        (27, 2, "=COUNTIF('POST LOG'!F:F,\"AGENT_NATIVE\")"),
        (27, 3, "=IFERROR(B27/B17,0)"),
        (28, 1, "TOOL_PROMO"),
        (28, 2, "=COUNTIF('POST LOG'!F:F,\"TOOL_PROMO\")"),
        (28, 3, "=IFERROR(B28/B17,0)"),
        (29, 1, "DEV_RECRUIT"),
        (29, 2, "=COUNTIF('POST LOG'!F:F,\"DEV_RECRUIT\")"),
        (29, 3, "=IFERROR(B29/B17,0)"),
        (30, 1, "CRYPTO_PITCH"),
        (30, 2, "=COUNTIF('POST LOG'!F:F,\"CRYPTO_PITCH\")"),
        (30, 3, "=IFERROR(B30/B17,0)"),
        (31, 1, "SOFT_SOCIAL"),
        (31, 2, "=COUNTIF('POST LOG'!F:F,\"SOFT_SOCIAL\")"),
        (31, 3, "=IFERROR(B31/B17,0)"),
        (32, 1, "REACTIVE"),
        (32, 2, "=COUNTIF('POST LOG'!F:F,\"REACTIVE\")"),
        (32, 3, "=IFERROR(B32/B17,0)"),

        # TOP SUBMOLTS section
        (34, 1, "── TOP 10 SUBMOLTS BY ROI GRADE ──"),
        (35, 1, '=IFERROR(QUERY(\'SUBMOLT PERFORMANCE\'!A:H,"SELECT A,B,E,H ORDER BY E DESC LIMIT 10",1),"Performance poller has not run yet.")'),

        # YEAR FORECAST PROGRESS section
        (46, 1, "── YEAR FORECAST PROGRESS (Feb 2026 → Feb 2027) ──"),
        (47, 1, "Year Target (posts)"),
        (47, 2, "=SUM('WEEKLY FORECAST'!C:C)"),
        (48, 1, "Year Actual (posts)"),
        (48, 2, "=B17"),
        (49, 1, "% Complete"),
        (49, 2, "=IFERROR(B48/B47,0)"),
        (50, 1, "Weeks Elapsed"),
        (50, 2, '=IFERROR(DATEDIF(DATE(2026,2,22),TODAY(),"W"),0)'),
        (51, 1, "Weeks Remaining"),
        (51, 2, "=MAX(0,53-B50)"),
        (52, 1, "Pace (posts/week)"),
        (52, 2, "=IFERROR(B48/B50,0)"),
        (53, 1, "Posts Needed/Week to Hit Target"),
        (53, 2, "=IFERROR((B47-B48)/B51,0)"),

        # NOTES / REFERENCES section
        (55, 1, "── NOTES / REFERENCES ──"),
        (56, 1, "Performance Poller"),
        (56, 2, "A2A subagent — runs every 2h via cron on snowdrop-node"),
        (57, 1, "ROI Grades"),
        (57, 2, "A=avg≥5 upvotes | B=avg≥2 | C=avg≥0.5 | D=avg>0 | F=avg=0"),
        (58, 1, "MiCA Regulation"),
        (58, 2, "EU 2023/1114 — token classification framework"),
        (59, 1, "FinCEN BOIR"),
        (59, 2, "31 U.S.C. § 5336 — beneficial ownership reporting"),
        (60, 1, "A2A Agent Card"),
        (60, 2, "https://snowdrop-mcp.fly.dev/.well-known/agent-performance-poller.json"),
    ]

    # Write all cells in one batch
    print("Writing formulas...")
    cell_list = []
    for row, col, value in cells_data:
        cell = gspread.Cell(row, col, value)
        cell_list.append(cell)
    ws.update_cells(cell_list, value_input_option="USER_ENTERED")

    # ── Formatting via Sheets API (batchUpdate) ───────────────────────────────
    print("Applying formatting...")
    sheet_id = ws.id

    requests_body = [
        # Header row: dark blue background, white bold text, large font
        {
            "repeatCell": {
                "range": {"sheetId": sheet_id, "startRowIndex": 0, "endRowIndex": 1,
                          "startColumnIndex": 0, "endColumnIndex": 4},
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": {"red": 0.07, "green": 0.18, "blue": 0.37},
                        "textFormat": {"foregroundColor": {"red": 1, "green": 1, "blue": 1},
                                       "bold": True, "fontSize": 13},
                        "horizontalAlignment": "LEFT",
                    }
                },
                "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)",
            }
        },
        # Section headers: medium blue background
        *[
            {
                "repeatCell": {
                    "range": {"sheetId": sheet_id, "startRowIndex": r - 1, "endRowIndex": r,
                              "startColumnIndex": 0, "endColumnIndex": 4},
                    "cell": {
                        "userEnteredFormat": {
                            "backgroundColor": {"red": 0.27, "green": 0.51, "blue": 0.71},
                            "textFormat": {"foregroundColor": {"red": 1, "green": 1, "blue": 1},
                                           "bold": True},
                        }
                    },
                    "fields": "userEnteredFormat(backgroundColor,textFormat)",
                }
            }
            for r in [3, 9, 16, 25, 34, 46, 55]
        ],
        # Bold label column (A)
        {
            "repeatCell": {
                "range": {"sheetId": sheet_id, "startRowIndex": 1, "endRowIndex": 60,
                          "startColumnIndex": 0, "endColumnIndex": 1},
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {"bold": True},
                    }
                },
                "fields": "userEnteredFormat.textFormat.bold",
            }
        },
        # % of Target (B13) — number format as percentage
        {
            "repeatCell": {
                "range": {"sheetId": sheet_id, "startRowIndex": 12, "endRowIndex": 13,
                          "startColumnIndex": 1, "endColumnIndex": 2},
                "cell": {
                    "userEnteredFormat": {
                        "numberFormat": {"type": "PERCENT", "pattern": "0.0%"},
                    }
                },
                "fields": "userEnteredFormat.numberFormat",
            }
        },
        # Engagement Rate (B20), % Complete (B49) — percentage format
        *[
            {
                "repeatCell": {
                    "range": {"sheetId": sheet_id, "startRowIndex": r - 1, "endRowIndex": r,
                              "startColumnIndex": 1, "endColumnIndex": 2},
                    "cell": {
                        "userEnteredFormat": {
                            "numberFormat": {"type": "PERCENT", "pattern": "0.0%"},
                        }
                    },
                    "fields": "userEnteredFormat.numberFormat",
                }
            }
            for r in [20, 26, 27, 28, 29, 30, 31, 32, 49]
        ],
        # Est. Token Cost (B23) — currency format
        {
            "repeatCell": {
                "range": {"sheetId": sheet_id, "startRowIndex": 22, "endRowIndex": 23,
                          "startColumnIndex": 1, "endColumnIndex": 2},
                "cell": {
                    "userEnteredFormat": {
                        "numberFormat": {"type": "CURRENCY", "pattern": "$#,##0.00"},
                    }
                },
                "fields": "userEnteredFormat.numberFormat",
            }
        },
        # Set column widths: A=220, B=200, C=180, D=120
        {"updateDimensionProperties": {
            "range": {"sheetId": sheet_id, "dimension": "COLUMNS", "startIndex": 0, "endIndex": 1},
            "properties": {"pixelSize": 220},
            "fields": "pixelSize",
        }},
        {"updateDimensionProperties": {
            "range": {"sheetId": sheet_id, "dimension": "COLUMNS", "startIndex": 1, "endIndex": 2},
            "properties": {"pixelSize": 200},
            "fields": "pixelSize",
        }},
        {"updateDimensionProperties": {
            "range": {"sheetId": sheet_id, "dimension": "COLUMNS", "startIndex": 2, "endIndex": 3},
            "properties": {"pixelSize": 180},
            "fields": "pixelSize",
        }},
        # Conditional format for "On Track?" cell (B14):
        # ✅ green if contains "On Track", ⚠️ yellow if "Behind", 🔴 red if "At Risk"
        {
            "addConditionalFormatRule": {
                "rule": {
                    "ranges": [{"sheetId": sheet_id, "startRowIndex": 13, "endRowIndex": 14,
                                "startColumnIndex": 1, "endColumnIndex": 2}],
                    "booleanRule": {
                        "condition": {"type": "TEXT_CONTAINS", "values": [{"userEnteredValue": "On Track"}]},
                        "format": {"backgroundColor": {"red": 0.71, "green": 0.91, "blue": 0.70}},
                    },
                },
                "index": 0,
            }
        },
        {
            "addConditionalFormatRule": {
                "rule": {
                    "ranges": [{"sheetId": sheet_id, "startRowIndex": 13, "endRowIndex": 14,
                                "startColumnIndex": 1, "endColumnIndex": 2}],
                    "booleanRule": {
                        "condition": {"type": "TEXT_CONTAINS", "values": [{"userEnteredValue": "Behind"}]},
                        "format": {"backgroundColor": {"red": 1.0, "green": 0.95, "blue": 0.60}},
                    },
                },
                "index": 1,
            }
        },
        {
            "addConditionalFormatRule": {
                "rule": {
                    "ranges": [{"sheetId": sheet_id, "startRowIndex": 13, "endRowIndex": 14,
                                "startColumnIndex": 1, "endColumnIndex": 2}],
                    "booleanRule": {
                        "condition": {"type": "TEXT_CONTAINS", "values": [{"userEnteredValue": "At Risk"}]},
                        "format": {"backgroundColor": {"red": 0.96, "green": 0.73, "blue": 0.73}},
                    },
                },
                "index": 2,
            }
        },
        # Freeze first row
        {
            "updateSheetProperties": {
                "properties": {
                    "sheetId": sheet_id,
                    "gridProperties": {"frozenRowCount": 1},
                },
                "fields": "gridProperties.frozenRowCount",
            }
        },
    ]

    wb.batch_update({"requests": requests_body})

    print(f"✅ DASHBOARD tab created and formatted successfully!")
    print(f"   Sheet: https://docs.google.com/spreadsheets/d/{SHEET_ID}")
    print(f"   All formulas auto-update from POST LOG, POST PERFORMANCE, WEEKLY FORECAST, SUBMOLT PERFORMANCE")


if __name__ == "__main__":
    main()
