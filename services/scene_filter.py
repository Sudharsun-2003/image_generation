from typing import List, Dict, Any
from models.scene import Scene
from services.orientation_service import OrientationService
from utils.constants import IMAGE_SLIDE_TYPE
from loguru import logger

class SceneFilter:
    def __init__(self, orientation_service: OrientationService):
        self.orientation_service = orientation_service

    def filter_image_slides(self, raw_scenes: List[Dict[str, Any]], video_id: str) -> List[Scene]:
        processed_scenes = []
        
        for scene_data in raw_scenes:
            metadata = scene_data.get("scene_metadata", {})
            scene_type = metadata.get("scene_type")
            
            if scene_type == IMAGE_SLIDE_TYPE:
                scene = self.build_processed_scene(scene_data, video_id)
                processed_scenes.append(scene)
                
        logger.info(f"Filtered {len(processed_scenes)} IMAGE_SLIDE scenes from {len(raw_scenes)} total scenes.")
        return processed_scenes

    def build_processed_scene(self, scene_data: Dict[str, Any], video_id: str) -> Scene:
        metadata = scene_data.get("scene_metadata", {})
        
        # Extract from metadata as per actual API structure
        template = metadata.get("scene_template", "")
        title = metadata.get("scene_title", "")
        
        # Determine orientation
        orientation = self.orientation_service.get_orientation(template)
        
        return Scene(
            video_id=video_id,
            scene_id=scene_data.get("scene_id", ""),
            scene_index=int(scene_data.get("scene_index", 0)),
            scene_title=title,
            scene_template=template,
            scene_type=metadata.get("scene_type", ""),
            orientation=orientation,
            narration=scene_data.get("narration", ""),
            narration_tamil=scene_data.get("narration_tamil", ""),
            duration=scene_data.get("duration", 0.0),
            upload_url=scene_data.get("upload_url")  # Preserved as requested
        )
