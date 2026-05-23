import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from utils.logger import logger

class FileHandler:
    @staticmethod
    def read_json(file_path: str) -> List[Dict[str, Any]]:
        path = Path(file_path)
        if not path.exists():
            logger.warning(f"File not found: {file_path}")
            return []
        
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    return []
                return json.loads(content)
        except Exception as e:
            logger.error(f"Error reading JSON file {file_path}: {e}")
            return []

    @staticmethod
    def write_json(file_path: str, data: Any) -> bool:
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            logger.error(f"Error writing JSON file {file_path}: {e}")
            return False

    @staticmethod
    def append_to_json(file_path: str, item: Dict[str, Any]) -> bool:
        data = FileHandler.read_json(file_path)
        data.append(item)
        return FileHandler.write_json(file_path, data)
