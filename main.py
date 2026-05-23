import os
import sys
from dotenv import load_dotenv
from loguru import logger

from utils.logger import setup_logger
from api.client import APIClient
from api.video_service import VideoService
from services.orientation_service import OrientationService
from services.scene_filter import SceneFilter
from services.storage_service import StorageService
from services.export_service import ExportService

def main():
    # 1. Load env
    load_dotenv()
    
    # 2. Initialize logger
    setup_logger()
    
    # Load configuration
    api_url = os.getenv("API_URL")
    bearer_token = os.getenv("BEARER_TOKEN")
    video_id = os.getenv("VIDEO_ID", "5415e24a") # Default from prompt if not in env
    
    if not api_url or not bearer_token:
        logger.error("API_URL or BEARER_TOKEN not found in .env file")
        sys.exit(1)

    logger.info("Starting AI Automation Pipeline")
    
    try:
        # Initialize Services
        api_client = APIClient(api_url, bearer_token)
        video_service = VideoService(api_client)
        orientation_service = OrientationService()
        scene_filter = SceneFilter(orientation_service)
        storage_service = StorageService()
        export_service = ExportService()

        # 3. Fetch video data
        raw_scenes = video_service.get_video(video_id)
        
        # 4 & 5. Filter IMAGE_SLIDE scenes & Determine orientation
        processed_scenes = scene_filter.filter_image_slides(raw_scenes, video_id)
        
        # 7. Create output/video_id folder
        video_dir = storage_service.prepare_video_storage(video_id)
        
        # Update scene paths for future images
        storage_service.update_scene_paths(processed_scenes)
        
        # 8. Export processed JSON
        json_output_path = video_dir / "processed_scenes.json"
        export_service.export_to_json(processed_scenes, json_output_path)
        
        # 9. Print summary
        print("\n" + "="*40)
        print("VIDEO PROCESSING COMPLETE")
        print("="*40)
        print(f"Video ID: {video_id}")
        print(f"Total Scenes: {len(raw_scenes)}")
        print(f"IMAGE_SLIDE Scenes: {len(processed_scenes)}")
        print("\nProcessed Scene IDs:")
        for scene in processed_scenes:
            print(f"* {scene.scene_id}")
            
        print(f"\nOutput JSON:\n{json_output_path}")
        
        print("\nFuture Image Paths:")
        for scene in processed_scenes:
            print(scene.image_path)
        print("="*40 + "\n")

    except Exception as e:
        logger.exception(f"An error occurred during execution: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
