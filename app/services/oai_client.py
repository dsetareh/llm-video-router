import asyncio
import httpx
import base64
from typing import List

AUDIO_API_URL = "http://192.168.1.22:11431/v1/chat/completions"
IMAGE_API_URL = "http://192.168.1.22:11430/v1/chat/completions"

async def get_audio_description(audio_path: str) -> str:
    """
    Sends an audio file to the OAI audio API and returns the description.
    """
    async with httpx.AsyncClient() as client:
        with open(audio_path, "rb") as f:
            audio_data = base64.b64encode(f.read()).decode("utf-8")
        
        payload = {
            "model": "llava",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Describe the audio."},
                        {"type": "image_url", "image_url": {"url": f"data:audio/mpeg;base64,{audio_data}"}}
                    ]
                }
            ]
        }
        
        response = await client.post(AUDIO_API_URL, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

async def get_frame_descriptions(image_paths: List[str]) -> List[str]:
    """
    Sends a list of image files to the OAI image API concurrently and returns their descriptions.
    """
    async with httpx.AsyncClient() as client:
        tasks = [_get_single_frame_description(client, path) for path in image_paths]
        descriptions = await asyncio.gather(*tasks)
        return descriptions

async def _get_single_frame_description(client: httpx.AsyncClient, image_path: str) -> str:
    """
    Helper function to get description for a single image.
    """
    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")
    
    payload = {
        "model": "llava",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Describe the image."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}}
                ]
            }
        ]
    }
    
    response = await client.post(IMAGE_API_URL, json=payload)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]