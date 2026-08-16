"""Agent One Configuration Constants"""

import os
from pathlib import Path

# API Configuration
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
GOOGLE_DRIVE_OAUTH_JSON = os.getenv("GOOGLE_DRIVE_OAUTH_JSON")
WHISPER_API_KEY = os.getenv("WHISPER_API_KEY")
DESCRIPT_API_KEY = os.getenv("DESCRIPT_API_KEY")
PIXABAY_API_KEY = os.getenv("PIXABAY_API_KEY")

# Google Drive Folder IDs (to be configured)
INBOX_FOLDER_ID = os.getenv("AGENT_ONE_INBOX_FOLDER_ID", "")
OUTBOX_FOLDER_ID = os.getenv("AGENT_ONE_OUTBOX_FOLDER_ID", "")
LOGS_FOLDER_ID = os.getenv("AGENT_ONE_LOGS_FOLDER_ID", "")
ERRORS_FOLDER_ID = os.getenv("AGENT_ONE_ERRORS_FOLDER_ID", "")

# Processing Configuration
PROCESSING_SCHEDULE_MINUTES = 30
MAX_RETRIES = 3
RETRY_BACKOFF_BASE = 2  # exponential backoff multiplier

# FFmpeg Settings
SILENCE_THRESHOLD_DB = -50
MIN_SILENCE_DURATION = 0.5  # seconds
AUDIO_NORMALIZATION_DB = -3
MUSIC_VOLUME_DB = -12

# Video Content Types
CONTENT_TYPES = {
    "meditation": {
        "silence_threshold": -50,
        "min_silence_duration": 2.0,
        "preserve_breathing": True,
    },
    "vlog": {
        "silence_threshold": -45,
        "min_silence_duration": 1.0,
        "preserve_breathing": False,
    },
    "speech": {
        "silence_threshold": -50,
        "min_silence_duration": 0.5,
        "preserve_breathing": False,
    },
    "interview": {
        "silence_threshold": -48,
        "min_silence_duration": 1.5,
        "preserve_breathing": False,
    },
}

# Platform Export Specifications
PLATFORM_SPECS = {
    "instagram": {
        "width": 1080,
        "height": 1350,
        "aspect_ratio": "4:5",
        "format": "mp4",
    },
    "tiktok": {
        "width": 1080,
        "height": 1920,
        "aspect_ratio": "9:16",
        "format": "mp4",
    },
    "youtube": {
        "width": 1080,
        "height": 1920,
        "aspect_ratio": "9:16",
        "format": "mp4",
    },
    "linkedin": {
        "width": 1200,
        "height": 628,
        "aspect_ratio": "16:9",
        "format": "mp4",
    },
}

# Caption Specifications by Platform
CAPTION_SPECS = {
    "instagram": {
        "min_words": 150,
        "max_words": 250,
        "style": "casual",
        "include_emojis": True,
        "hook_required": True,
    },
    "tiktok": {
        "min_words": 50,
        "max_words": 100,
        "style": "pattern_interrupt",
        "include_emojis": True,
        "trending_angle": True,
    },
    "youtube": {
        "min_words": 200,
        "max_words": None,
        "style": "educational",
        "include_keywords": True,
        "seo_focused": True,
    },
    "linkedin": {
        "min_words": 150,
        "max_words": 200,
        "style": "professional",
        "include_emojis": False,
        "professional_tone": True,
    },
}

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
LOGS_DIR = PROJECT_ROOT / "logs"
TEMP_DIR = PROJECT_ROOT / "temp"
CACHE_DIR = PROJECT_ROOT / "cache"

# Ensure directories exist
for directory in [LOGS_DIR, TEMP_DIR, CACHE_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# State Files
COMPLETED_VIDEOS_FILE = LOGS_DIR / "completed_videos.json"
CURRENT_JOBS_FILE = LOGS_DIR / "current_jobs.json"
