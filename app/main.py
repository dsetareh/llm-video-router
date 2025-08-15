import asyncio
import os
from fastapi import FastAPI, HTTPException
from app.schemas import VideoURLRequest, ProcessingResponse
from app.services.video_downloader import download_video
from app.services.video_processor import extract_audio, extract_frames
from app.services.oai_client import get_audio_description, get_frame_descriptions

app = FastAPI()

@app.post("/process_video", response_model=ProcessingResponse)
async def process_video(request: VideoURLRequest):
    video_path = None
    audio_path = None
    frame_paths = []
    try:
        # Download video
        video_path = await download_video(request.video_url)
        if not video_path:
            raise HTTPException(status_code=400, detail="Failed to download video")

        # Process video
        audio_path = await extract_audio(video_path)
        frame_paths = await extract_frames(video_path)

        if not audio_path or not frame_paths:
            raise HTTPException(status_code=500, detail="Failed to process video")

        # Get descriptions concurrently
        audio_desc_task = get_audio_description(audio_path)
        frame_descs_task = get_frame_descriptions(frame_paths)

        audio_description, frame_descriptions = await asyncio.gather(
            audio_desc_task, frame_descs_task
        )

        return ProcessingResponse(
            audio_description=audio_description,
            frame_descriptions=frame_descriptions,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Cleanup
        if video_path and os.path.exists(video_path):
            os.remove(video_path)
        if audio_path and os.path.exists(audio_path):
            os.remove(audio_path)
        for frame_path in frame_paths:
            if os.path.exists(frame_path):
                os.remove(frame_path)