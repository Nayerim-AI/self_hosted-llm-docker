## pipeline/youtube_agent.py
import requests

def get_comments(video_id, api_key, max_results=100):  # <= Turunkan jadi 5
    url = "https://www.googleapis.com/youtube/v3/commentThreads"
    params = {
        "part": "snippet",
        "videoId": video_id,
        "maxResults": max_results,
        "key": api_key,
        "textFormat": "plainText"
    }
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        items = response.json().get("items", [])
        comments = [
            item["snippet"]["topLevelComment"]["snippet"]["textDisplay"][:200]  # batasi panjang komentar
            for item in items
        ]
        return comments
    except Exception as e:
        print(f"[YouTube API Error] {e}")
        return []
