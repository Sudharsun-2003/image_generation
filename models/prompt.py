from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class PromptOutput(BaseModel):
    prompt: str
    background: str
    orientation: str

class ScenePrompt(BaseModel):
    scene_id: str
    video_id: str
    prompt: str
    background: str
    orientation: str
    original_narration: str
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
