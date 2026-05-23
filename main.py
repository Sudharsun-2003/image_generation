import os
import sys
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from loguru import logger

from utils.logger import setup_logger
from api.client import APIClient
from api.video_service import VideoService
from services.orientation_service import OrientationService
from services.scene_filter import SceneFilter
from services.storage_service import StorageService
from services.export_service import ExportService

# Phase 2 Imports
from services.api_client import GroqClient
from services.prompt_generator import PromptGenerator

async def run_pipeline():
    # 1. Load env
    load_dotenv()
    
    # 2. Initialize logger
    setup_logger()
    
    # Load configuration
    api_url = os.getenv("API_URL")
    bearer_token = os.getenv("BEARER_TOKEN")
    video_id = os.getenv("VIDEO_ID")
    groq_api_key = os.getenv("GROQ_API_KEY")

    if not video_id:
        logger.error("VIDEO_ID not found in .env file or environment.")
        return
    
    logger.info(f"Starting AI Automation Pipeline for Video ID: {video_id}")

    # Setup Paths
    output_dir = Path(f"output/{video_id}")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    scenes_path = output_dir / "processed_scenes.json"
    prompts_path = output_dir / "prompts.json"

    # PHASE 1: Scene Extraction
    if not scenes_path.exists():
        if not api_url or not bearer_token:
            logger.error("API_URL or BEARER_TOKEN not found in .env file")
            return

        try:
            logger.info(f"Starting Phase 1: Scene Extraction for {video_id}")
            # Initialize Services
            api_client = APIClient(api_url, bearer_token)
            video_service = VideoService(api_client)
            orientation_service = OrientationService()
            scene_filter = SceneFilter(orientation_service)
            export_service = ExportService()

            # Fetch video data
            raw_scenes = video_service.get_video(video_id)
            
            # Filter IMAGE_SLIDE scenes & Determine orientation
            processed_scenes = scene_filter.filter_image_slides(raw_scenes, video_id)
            
            # Export processed JSON to output/{video_id}/processed_scenes.json
            export_service.export_to_json(processed_scenes, scenes_path)
            logger.info(f"Phase 1 Complete: {len(processed_scenes)} scenes saved to {scenes_path}")

        except Exception as e:
            logger.exception(f"An error occurred during Phase 1: {e}")
            return
    else:
        logger.info(f"Skipping Phase 1, using existing {scenes_path}")

    # PHASE 2: Prompt Generation
    if not groq_api_key:
        logger.error("GROQ_API_KEY not found in .env file. Skipping Phase 2.")
        return

    try:
        logger.info(f"Starting Phase 2: Prompt Generation for {video_id}")
        groq_client = GroqClient(api_key=groq_api_key)
        prompt_gen = PromptGenerator(
            groq_client=groq_client,
            scenes_path=str(scenes_path),
            prompts_path=str(prompts_path)
        )
        
        await prompt_gen.process_scenes(batch_size=3)
        logger.info(f"Phase 2 Complete: Prompts saved to {prompts_path}")

    except Exception as e:
        logger.exception(f"An error occurred during Phase 2: {e}")

def main():
    asyncio.run(run_pipeline())

if __name__ == "__main__":
    main()
