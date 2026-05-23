from typing import List, Dict, Any
from api.client import APIClient
from loguru import logger

class VideoService:
    def __init__(self, api_client: APIClient):
        self.api_client = api_client

    def get_video(self, video_id: str) -> List[Dict[str, Any]]:
        payload = {
            "action": "get_video",
            "video_id": video_id
        }
        
        logger.info(f"Fetching video data for ID: {video_id}")
        response_data = self.api_client.post(payload)
        
        logger.debug(f"Raw API Response: {response_data}")
        
        # The API returns scenes inside the 'data' object
        data = response_data.get("data", {})
        scenes = data.get("scenes", [])
        
        if not scenes:
            logger.warning(f"No scenes found in 'data' for video_id: {video_id}")
            
        return scenes
