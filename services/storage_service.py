from pathlib import Path
from loguru import logger
from models.scene import Scene

class StorageService:
    def __init__(self, base_output_dir: str = "output"):
        self.base_dir = Path(base_output_dir)

    def prepare_video_storage(self, video_id: str) -> Path:
        video_dir = self.base_dir / video_id
        video_dir.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Prepared storage directory: {video_dir}")
        return video_dir

    def get_image_path(self, video_id: str, scene_id: str) -> str:
        return str(self.base_dir / video_id / f"{scene_id}.png")

    def update_scene_paths(self, scenes: list[Scene]) -> None:
        for scene in scenes:
            scene.image_path = self.get_image_path(scene.video_id, scene.scene_id)
