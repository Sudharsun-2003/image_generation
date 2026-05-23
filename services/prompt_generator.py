import asyncio
from typing import List, Dict, Any, Set, Optional
from utils.logger import logger
from utils.file_handler import FileHandler
from services.api_client import GroqClient
from models.prompt import ScenePrompt, PromptOutput

class PromptGenerator:
    SYSTEM_PROMPT = """You are an expert AI visual prompt engineer.
Convert educational narration into clean infographic-style image prompts.
RULES:
- Keep prompts concise
- Focus on visual storytelling
- Modern flat design
- Minimal text
- No paragraph text inside image
- Educational infographic style
- Mention orientation
- Mention layout
- Mention key visual elements
- Mention minimal labels only
- Use clean tech illustration aesthetics
- Use uncluttered composition- Use pastel backgrounds
- Avoid realism
- Avoid cinematic style
Return ONLY valid JSON.
Format:
{
  "prompt": "...",
  "background": "...",
  "orientation": "..."
}"""

    def __init__(self, groq_client: GroqClient, scenes_path: str, prompts_path: str):
        self.client = groq_client
        self.scenes_path = scenes_path
        self.prompts_path = prompts_path
        self.processed_ids: Set[str] = self._get_processed_ids()

    def _get_processed_ids(self) -> Set[str]:
        existing_prompts = FileHandler.read_json(self.prompts_path)
        return {p["scene_id"] for p in existing_prompts}

    async def process_scenes(self, batch_size: int = 5):
        scenes = FileHandler.read_json(self.scenes_path)
        # Filter IMAGE_SLIDE scenes and those not yet processed
        to_process = [
            s for s in scenes 
            if s.get("scene_type") == "IMAGE_SLIDE" and s["scene_id"] not in self.processed_ids
        ]

        if not to_process:
            logger.info("No new IMAGE_SLIDE scenes to process.")
            return

        logger.info(f"Found {len(to_process)} scenes to process.")

        # Batch processing
        for i in range(0, len(to_process), batch_size):
            batch = to_process[i:i + batch_size]
            tasks = [self.process_single_scene(scene) for scene in batch]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for result in results:
                if isinstance(result, Exception):
                    logger.error(f"Failed to process scene: {result}")
                elif result:
                    # Incremental save
                    FileHandler.append_to_json(self.prompts_path, result.model_dump())
                    self.processed_ids.add(result.scene_id)

    async def process_single_scene(self, scene: Dict[str, Any]) -> Optional[ScenePrompt]:
        scene_id = scene["scene_id"]
        narration = scene.get("narration", "")
        orientation = scene.get("orientation", "square")
        
        if not narration:
            logger.warning(f"No narration found for scene: {scene_id}")
            return None

        logger.info(f"Generating prompt for scene: {scene_id}")
        
        user_prompt = f"Narration:\n{narration}\nOrientation:\n{orientation}"
        
        try:
            raw_output = await self.client.generate_completion(self.SYSTEM_PROMPT, user_prompt)
            # Validate output with Pydantic
            prompt_data = PromptOutput(**raw_output)
            
            return ScenePrompt(
                scene_id=scene_id,
                video_id=scene["video_id"],
                prompt=prompt_data.prompt,
                background=prompt_data.background,
                orientation=prompt_data.orientation,
                original_narration=narration
            )
        except Exception as e:
            logger.error(f"Error processing scene {scene_id}: {e}")
            return None
