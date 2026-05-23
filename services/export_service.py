import json
from pathlib import Path
from typing import List
from models.scene import Scene
from loguru import logger

class ExportService:
    @staticmethod
    def export_to_json(scenes: List[Scene], output_path: Path) -> None:
        data = [scene.to_dict() for scene in scenes]
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            
        logger.info(f"Exported {len(scenes)} scenes to {output_path}")
