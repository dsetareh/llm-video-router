# video ai but bad

## Description
This is a FastAPI application that accepts a video URL, downloads the video, extracts audio and frames, and uses two separate OAI-compatible APIs to generate descriptions for them.

## Features
- Video download from URL
- Audio extraction from video
- Frame generation from video
- Integration with OAI-compatible APIs for audio and frame description

## API Usage

### Endpoint
`POST /process_video`

### Request Body
```json
{
  "video_url": "https://example.com/video.mp4"
}
```

**Note on API Behavior:** This API operates on a synchronous request/response model. The connection is held open until all video processing is complete, and the result is returned directly in the response to the initial request.

### Example Success Response
```json
{
  "audio_description": "A description of the audio content.",
  "frame_descriptions": [
    "A description of the first frame.",
    "A description of the second frame.",
    "..."
  ]
}
```

### Example `curl` Command
```bash
curl -X POST "http://localhost:8000/process_video" -H "Content-Type: application/json" -d '{"video_url": "https://example.com/video.mp4"}'
```

## Setup and Installation
1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the application:**
    ```bash
    uvicorn app.main:app --reload
    ```

## Project Structure
```
app/
├── main.py
├── schemas.py
└── services/
    ├── oai_client.py
    ├── video_downloader.py
    └── video_processor.py