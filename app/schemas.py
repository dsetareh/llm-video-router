from pydantic import BaseModel
from typing import List

class VideoURLRequest(BaseModel):
    video_url: str

class ProcessingResponse(BaseModel):
    audio_description: str
    frame_descriptions: List[str]