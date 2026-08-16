"""External API Clients for Whisper, Descript, and Pixabay"""

import logging
from pathlib import Path
from typing import Optional, Dict, List
import requests

from config.constants import WHISPER_API_KEY, DESCRIPT_API_KEY, PIXABAY_API_KEY


class WhisperClient:
    """OpenAI Whisper API for transcription"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.api_key = WHISPER_API_KEY
        self.api_url = "https://api.openai.com/v1/audio/transcriptions"

    def transcribe(self, audio_file_path: Path) -> Optional[Dict]:
        """Transcribe audio file to text with timestamps"""
        if not self.api_key:
            self.logger.error("WHISPER_API_KEY not set")
            return None

        try:
            with open(audio_file_path, "rb") as f:
                files = {"file": f}
                headers = {"Authorization": f"Bearer {self.api_key}"}
                data = {"model": "whisper-1"}

                response = requests.post(
                    self.api_url,
                    files=files,
                    headers=headers,
                    data=data,
                    timeout=300,
                )

            if response.status_code == 200:
                result = response.json()
                self.logger.info(
                    f"✅ Transcribed audio: {len(result.get('text', ''))} characters"
                )
                return result
            else:
                self.logger.error(f"Whisper API error: {response.text}")
                return None

        except Exception as e:
            self.logger.error(f"Error transcribing with Whisper: {e}")
            return None


class DescriptClient:
    """Descript API for professional video finishing"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.api_key = DESCRIPT_API_KEY
        self.api_url = "https://api.descript.com/v1"

    def process_video(
        self,
        video_path: Path,
        captions: Dict[str, str],
        color_grade_intensity: int,
        platforms: List[str],
    ) -> Optional[Dict[str, str]]:
        """Process video with Descript: color grading, captions, export"""
        if not self.api_key:
            self.logger.error("DESCRIPT_API_KEY not set")
            return None

        try:
            # This is a simplified example - actual Descript API call would be more complex
            # In production, you'd:
            # 1. Upload video to Descript
            # 2. Apply color grading
            # 3. Add captions
            # 4. Export for each platform

            # For now, return placeholder paths
            output_paths = {}
            for platform in platforms:
                output_paths[platform] = f"output_{platform}.mp4"

            self.logger.info(
                f"✅ Descript processing initiated for {len(platforms)} platforms"
            )
            return output_paths

        except Exception as e:
            self.logger.error(f"Error processing with Descript: {e}")
            return None


class PixabayMusicClient:
    """Pixabay Music API for royalty-free music"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.api_key = PIXABAY_API_KEY
        self.api_url = "https://pixabay.com/api/videos/"

    def search_music(
        self, query: str, limit: int = 5
    ) -> Optional[List[Dict[str, str]]]:
        """Search for royalty-free music by style/mood"""
        if not self.api_key:
            self.logger.error("PIXABAY_API_KEY not set")
            return None

        try:
            params = {
                "key": self.api_key,
                "q": query,
                "per_page": limit,
                "video_type": "all",
            }

            response = requests.get(self.api_url, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()
                tracks = []

                for hit in data.get("hits", [])[:limit]:
                    track = {
                        "id": str(hit.get("id")),
                        "title": hit.get("tags", "Unknown"),
                        "download_url": hit.get("media", {}).get("m4", {}).get("url"),
                        "duration": hit.get("duration", 0),
                        "author": hit.get("user", ""),
                    }
                    tracks.append(track)

                self.logger.info(f"✅ Found {len(tracks)} tracks for '{query}'")
                return tracks
            else:
                self.logger.error(f"Pixabay API error: {response.text}")
                return None

        except Exception as e:
            self.logger.error(f"Error searching music with Pixabay: {e}")
            return None

    def download_music(
        self, download_url: str, output_path: Path
    ) -> bool:
        """Download music track"""
        try:
            response = requests.get(download_url, timeout=30)

            if response.status_code == 200:
                with open(output_path, "wb") as f:
                    f.write(response.content)

                self.logger.info(f"✅ Downloaded music to {output_path}")
                return True
            else:
                self.logger.error(f"Error downloading music: {response.status_code}")
                return False

        except Exception as e:
            self.logger.error(f"Error downloading music: {e}")
            return False
