import os
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize MCP server
mcp = FastMCP(
    "YouTube MCP Server",
    host="0.0.0.0",
    port=7040
)

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

BASE_URL = "https://www.googleapis.com/youtube/v3"


async def _get(endpoint: str, params: dict):
    params["key"] = YOUTUBE_API_KEY
    async with httpx.AsyncClient() as client:
        res = await client.get(f"{BASE_URL}/{endpoint}", params=params)
        if res.status_code >= 400:
            raise Exception(f"YouTube API Error: {res.text}")
        return res.json()


# -----------------------------
# LIST / SEARCH VIDEOS
# -----------------------------
@mcp.tool()
async def search_videos(query: str, max_results: int = 5):
    """
    Search for YouTube videos by keyword.
    """
    data = await _get("search", {
        "part": "snippet",
        "q": query,
        "maxResults": max_results,
        "type": "video"
    })

    results = []
    for item in data.get("items", []):
        results.append({
            "video_id": item["id"]["videoId"],
            "title": item["snippet"]["title"],
            "channel": item["snippet"]["channelTitle"]
        })

    return results


# -----------------------------
# GET VIDEO DETAILS
# -----------------------------
@mcp.tool()
async def get_video_details(video_id: str):
    """
    Get detailed information about a video.
    """
    data = await _get("videos", {
        "part": "snippet,statistics",
        "id": video_id
    })

    if not data.get("items"):
        return "Video not found"

    item = data["items"][0]

    return {
        "title": item["snippet"]["title"],
        "description": item["snippet"]["description"],
        "channel": item["snippet"]["channelTitle"],
        "views": item["statistics"].get("viewCount"),
        "likes": item["statistics"].get("likeCount")
    }


# -----------------------------
# GET COMMENTS (REVIEWS)
# -----------------------------
@mcp.tool()
async def get_video_comments(video_id: str, max_results: int = 5):
    """
    Get top comments for a video.
    """
    data = await _get("commentThreads", {
        "part": "snippet",
        "videoId": video_id,
        "maxResults": max_results
    })

    comments = []
    for item in data.get("items", []):
        snippet = item["snippet"]["topLevelComment"]["snippet"]
        comments.append({
            "author": snippet["authorDisplayName"],
            "comment": snippet["textDisplay"],
            "likes": snippet["likeCount"]
        })

    return comments


# -----------------------------
# PLACEHOLDER: UPDATE VIDEO
# -----------------------------
@mcp.tool()
async def update_video_metadata(video_id: str, title: str, description: str):
    """
    Update video metadata (Requires OAuth 2.0).
    """
    return "⚠️ This operation requires OAuth 2.0 authentication (not API key)."


# -----------------------------
# PLACEHOLDER: DELETE VIDEO
# -----------------------------
@mcp.tool()
async def delete_video(video_id: str):
    """
    Delete a video (Requires OAuth 2.0).
    """
    return "⚠️ This operation requires OAuth 2.0 authentication (not API key)."


# -----------------------------
# RUN SERVER
# -----------------------------
if __name__ == "__main__":
    if not YOUTUBE_API_KEY:
        raise Exception("Set YOUTUBE_API_KEY as environment variable")
    mcp.run(transport="streamable-http")
