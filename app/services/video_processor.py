import os
import tempfile
from typing import List
import cv2
from moviepy.editor import VideoFileClip

def extract_audio(video_path: str) -> str:
    """
    Extracts the audio from a video file.

    Args:
        video_path: The path to the video file.

    Returns:
        The path to the extracted audio file.
    """
    video_clip = VideoFileClip(video_path)
    audio_clip = video_clip.audio
    temp_dir = tempfile.mkdtemp()
    audio_file_path = os.path.join(temp_dir, "audio.mp3")
    audio_clip.write_audiofile(audio_file_path)
    audio_clip.close()
    video_clip.close()
    return audio_file_path

def extract_frames(video_path: str) -> List[str]:
    """
    Extracts 6 frames from a video at evenly distributed intervals.

    Args:
        video_path: The path to the video file.

    Returns:
        A list of file paths for the extracted frames.
    """
    temp_dir = tempfile.mkdtemp()
    video_capture = cv2.VideoCapture(video_path)
    total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_paths = []
    
    for i in range(6):
        frame_number = int(total_frames * (i + 1) / 6.0)
        video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame_number - 1)
        success, image = video_capture.read()
        if success:
            frame_path = os.path.join(temp_dir, f"frame_{i+1}.jpg")
            cv2.imwrite(frame_path, image)
            frame_paths.append(frame_path)
            
    video_capture.release()
    return frame_paths