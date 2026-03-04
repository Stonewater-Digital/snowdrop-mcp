"""
A/B Test Analytics Engine for Moltbook posts.
Calculates engagement win rates between Gemini 2.0 Flash-Lite and Grok 4.1 Fast.
"""
import logging
from collections import defaultdict
from typing import List, Dict

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "get_ab_test_insights",
    "description": "Calculates Moltbook engagement win rates comparing Gemini 2.0 Flash-Lite and Grok 4.1 Fast based on historical performance.",
    "inputSchema": {
        "type": "object",
        "properties": {},
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {"type": "object"},
            "message": {"type": "string"}
        },
        "required": ["status"],
    },
}

def calculate_win_rates(merged_data: List[Dict]) -> Dict:
    """
    Calculates engagement metrics split by LLM model.
    
    Args:
        merged_data: List of dicts with keys: 'model', 'upvotes', 'comments', 'date'
        
    Returns:
        Dict mapping timeframes to model performance stats.
    """
    results = {
        "all_time": defaultdict(lambda: {"total_posts": 0, "total_upvotes": 0, "total_comments": 0})
    }
    
    for row in merged_data:
        model = row.get("model")
        if not model or model == "fallback-template":
            continue
            
        upvotes = int(row.get("upvotes", 0) or 0)
        comments = int(row.get("comments", 0) or 0)
        
        stats = results["all_time"][model]
        stats["total_posts"] += 1
        stats["total_upvotes"] += upvotes
        stats["total_comments"] += comments
        
    # Calculate averages
    for model, stats in results["all_time"].items():
        if stats["total_posts"] > 0:
            stats["avg_upvotes"] = stats["total_upvotes"] / stats["total_posts"]
            stats["avg_comments"] = stats["total_comments"] / stats["total_posts"]
        else:
            stats["avg_upvotes"] = 0.0
            stats["avg_comments"] = 0.0
            
    # Convert defaultdict to dict for cleaner output
    results["all_time"] = dict(results["all_time"])
    return results

def get_ab_test_insights() -> dict:
    """
    MCP tool entry point to read sheet and return A/B test results.
    """
    from skills.social.moltbook_engagement_sheet import _get_client, SHEET_ID, TAB_POST_LOG, TAB_PERFORMANCE
    
    try:
        gc = _get_client()
        sheet = gc.open_by_key(SHEET_ID)
        
        # Read data
        ws_log = sheet.worksheet(TAB_POST_LOG)
        ws_perf = sheet.worksheet(TAB_PERFORMANCE)
        
        log_rows = ws_log.get_all_records()
        perf_rows = ws_perf.get_all_records()
        
        # Merge on Post ID
        perf_map = {str(r.get("Post ID", "")): {"upvotes": r.get("Upvotes", 0), "comments": r.get("Comments", 0)} for r in perf_rows if "Post ID" in r}
        
        merged_data = []
        for r in log_rows:
            post_id = str(r.get("Post ID", ""))
            perf = perf_map.get(post_id, {"upvotes": 0, "comments": 0})
            merged_data.append({
                "model": r.get("Model", ""),
                "date": r.get("Date", ""),
                "upvotes": perf["upvotes"],
                "comments": perf["comments"]
            })
            
        return {
            "status": "success",
            "data": calculate_win_rates(merged_data)
        }
        
    except Exception as e:
        logger.error(f"Failed to generate A/B insights: {e}")
        return {
            "status": "error",
            "message": str(e)
        }
