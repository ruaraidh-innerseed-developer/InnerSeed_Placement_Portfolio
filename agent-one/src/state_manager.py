"""State Management for Agent One - Handles persistent state and logging"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict, field

from config.constants import COMPLETED_VIDEOS_FILE, CURRENT_JOBS_FILE, LOGS_DIR


@dataclass
class ProcessingJob:
    """Represents a video processing job"""
    video_id: str
    video_name: str
    brief_name: str
    status: str  # pending, processing, completed, failed
    created_at: str
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    error_message: Optional[str] = None
    processing_time_minutes: Optional[float] = None
    content_type: Optional[str] = None
    platforms: List[str] = field(default_factory=list)
    output_paths: Dict[str, str] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return asdict(self)

    @staticmethod
    def from_dict(data: Dict) -> "ProcessingJob":
        return ProcessingJob(**data)


class StateManager:
    """Manages persistent state for Agent One"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.completed_videos: Dict[str, Dict] = self._load_completed_videos()
        self.current_jobs: Dict[str, ProcessingJob] = self._load_current_jobs()
        self._setup_daily_log()

    def _load_completed_videos(self) -> Dict[str, Dict]:
        """Load list of completed videos to prevent re-processing"""
        if not COMPLETED_VIDEOS_FILE.exists():
            return {}
        try:
            with open(COMPLETED_VIDEOS_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading completed videos: {e}")
            return {}

    def _save_completed_videos(self):
        """Save completed videos list"""
        try:
            with open(COMPLETED_VIDEOS_FILE, "w") as f:
                json.dump(self.completed_videos, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving completed videos: {e}")

    def _load_current_jobs(self) -> Dict[str, ProcessingJob]:
        """Load current jobs in progress"""
        if not CURRENT_JOBS_FILE.exists():
            return {}
        try:
            with open(CURRENT_JOBS_FILE, "r") as f:
                data = json.load(f)
                return {
                    job_id: ProcessingJob.from_dict(job_data)
                    for job_id, job_data in data.items()
                }
        except Exception as e:
            self.logger.error(f"Error loading current jobs: {e}")
            return {}

    def _save_current_jobs(self):
        """Save current jobs"""
        try:
            data = {job_id: job.to_dict() for job_id, job in self.current_jobs.items()}
            with open(CURRENT_JOBS_FILE, "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving current jobs: {e}")

    def _setup_daily_log(self):
        """Setup daily logging file"""
        today = datetime.now().strftime("%Y-%m-%d")
        self.daily_log_file = LOGS_DIR / f"processing_log_{today}.txt"

    def is_video_processed(self, video_name: str) -> bool:
        """Check if video has already been processed"""
        return video_name in self.completed_videos

    def add_completed_video(
        self, video_name: str, metadata: Dict[str, Any], platforms: List[str]
    ) -> None:
        """Record a completed video"""
        self.completed_videos[video_name] = {
            "completed_at": datetime.now().isoformat(),
            "metadata": metadata,
            "platforms": platforms,
        }
        self._save_completed_videos()
        self.log_activity(f"✅ Video completed: {video_name}")

    def create_job(
        self, video_id: str, video_name: str, brief_name: str
    ) -> ProcessingJob:
        """Create a new processing job"""
        job = ProcessingJob(
            video_id=video_id,
            video_name=video_name,
            brief_name=brief_name,
            status="pending",
            created_at=datetime.now().isoformat(),
        )
        self.current_jobs[video_id] = job
        self._save_current_jobs()
        self.log_activity(f"📋 New job created: {video_name}")
        return job

    def update_job(self, job_id: str, **kwargs) -> None:
        """Update a job's status and metadata"""
        if job_id not in self.current_jobs:
            self.logger.error(f"Job {job_id} not found")
            return

        job = self.current_jobs[job_id]
        for key, value in kwargs.items():
            if hasattr(job, key):
                setattr(job, key, value)

        self._save_current_jobs()

    def complete_job(
        self, job_id: str, output_paths: Dict[str, str], processing_time: float
    ) -> None:
        """Mark a job as completed"""
        if job_id not in self.current_jobs:
            self.logger.error(f"Job {job_id} not found")
            return

        job = self.current_jobs[job_id]
        job.status = "completed"
        job.completed_at = datetime.now().isoformat()
        job.output_paths = output_paths
        job.processing_time_minutes = processing_time

        # Move to completed videos
        self.add_completed_video(job.video_name, job.to_dict(), job.platforms)
        # Remove from current jobs
        del self.current_jobs[job_id]
        self._save_current_jobs()

    def fail_job(self, job_id: str, error_message: str) -> None:
        """Mark a job as failed"""
        if job_id not in self.current_jobs:
            self.logger.error(f"Job {job_id} not found")
            return

        job = self.current_jobs[job_id]
        job.status = "failed"
        job.error_message = error_message
        job.completed_at = datetime.now().isoformat()

        self._save_current_jobs()
        self.log_activity(f"❌ Job failed: {job.video_name} - {error_message}")

    def log_activity(self, message: str) -> None:
        """Log activity to daily log file"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"

        try:
            with open(self.daily_log_file, "a") as f:
                f.write(log_entry)
        except Exception as e:
            self.logger.error(f"Error writing to log file: {e}")

    def get_job_status(self, job_id: str) -> Optional[ProcessingJob]:
        """Get current status of a job"""
        return self.current_jobs.get(job_id)

    def get_all_current_jobs(self) -> List[ProcessingJob]:
        """Get all jobs currently in progress"""
        return list(self.current_jobs.values())

    def get_completed_videos_today(self) -> List[str]:
        """Get list of videos completed today"""
        today = datetime.now().strftime("%Y-%m-%d")
        completed_today = []
        for video_name, info in self.completed_videos.items():
            if info["completed_at"].startswith(today):
                completed_today.append(video_name)
        return completed_today
