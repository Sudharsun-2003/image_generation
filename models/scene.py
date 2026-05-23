from dataclasses import dataclass, field
from typing import Optional, Dict, Any

@dataclass
class Scene:
    video_id: str
    scene_id: str
    scene_index: int
    scene_title: str
    scene_template: str
    scene_type: str
    orientation: str
    narration: str
    narration_tamil: str
    duration: float
    image_path: Optional[str] = None
    upload_url: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "video_id": self.video_id,
            "scene_id": self.scene_id,
            "scene_index": self.scene_index,
            "scene_title": self.scene_title,
            "scene_template": self.scene_template,
            "scene_type": self.scene_type,
            "orientation": self.orientation,
            "narration": self.narration,
            "narration_tamil": self.narration_tamil,
            "duration": self.duration,
            "image_path": self.image_path
        }
