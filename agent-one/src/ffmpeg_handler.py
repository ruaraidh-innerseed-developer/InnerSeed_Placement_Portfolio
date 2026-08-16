"""FFmpeg Handler for video processing and analysis"""

import logging
import subprocess
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

from config.constants import (
    SILENCE_THRESHOLD_DB,
    MIN_SILENCE_DURATION,
    AUDIO_NORMALIZATION_DB,
    MUSIC_VOLUME_DB,
    PLATFORM_SPECS,
)


@dataclass
class SilenceSegment:
    """Represents a silence segment in audio"""

    start: float
    end: float
    duration: float


@dataclass
class VideoMetadata:
    """Metadata about a video"""

    duration: float
    width: int
    height: int
    fps: float
    audio_channels: int
    audio_sample_rate: int


class FFmpegHandler:
    """Handles all FFmpeg operations"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._check_ffmpeg()

    def _check_ffmpeg(self) -> bool:
        """Check if FFmpeg is available"""
        try:
            result = subprocess.run(
                ["ffmpeg", "-version"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode == 0:
                self.logger.info("✅ FFmpeg is available")
                return True
        except Exception as e:
            self.logger.error(f"FFmpeg not found: {e}")
            return False

    def get_video_metadata(self, video_path: Path) -> Optional[VideoMetadata]:
        """Extract metadata from video file"""
        try:
            cmd = [
                "ffprobe",
                "-v",
                "error",
                "-show_format",
                "-show_streams",
                "-of",
                "json",
                str(video_path),
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

            if result.returncode != 0:
                self.logger.error(f"Error probing video: {result.stderr}")
                return None

            data = json.loads(result.stdout)

            # Extract video and audio streams
            video_stream = None
            audio_stream = None

            for stream in data.get("streams", []):
                if stream["codec_type"] == "video":
                    video_stream = stream
                elif stream["codec_type"] == "audio":
                    audio_stream = stream

            if not video_stream:
                self.logger.error("No video stream found")
                return None

            metadata = VideoMetadata(
                duration=float(data["format"].get("duration", 0)),
                width=video_stream.get("width", 0),
                height=video_stream.get("height", 0),
                fps=eval(video_stream.get("r_frame_rate", "30/1")),
                audio_channels=audio_stream.get("channels", 0) if audio_stream else 0,
                audio_sample_rate=audio_stream.get("sample_rate", 0)
                if audio_stream
                else 0,
            )

            self.logger.info(f"Video metadata: {metadata.duration}s, {metadata.width}x{metadata.height}")
            return metadata

        except Exception as e:
            self.logger.error(f"Error getting video metadata: {e}")
            return None

    def detect_silence(
        self,
        video_path: Path,
        threshold_db: float = SILENCE_THRESHOLD_DB,
        min_duration: float = MIN_SILENCE_DURATION,
    ) -> List[SilenceSegment]:
        """Detect silence segments in video audio"""
        try:
            cmd = [
                "ffmpeg",
                "-i",
                str(video_path),
                "-af",
                f"silencedetect=n={threshold_db}dB:d={min_duration}",
                "-f",
                "null",
                "-",
            ]

            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=120
            )

            # Parse output for silence segments
            silence_segments = []
            lines = result.stderr.split("\n")

            for line in lines:
                if "silence_start" in line:
                    parts = line.split()
                    for i, part in enumerate(parts):
                        if part.startswith("silence_start:"):
                            start = float(part.split(":")[-1])
                            # Find corresponding end
                            for end_line in lines:
                                if "silence_end" in end_line and start in end_line:
                                    end_parts = end_line.split()
                                    for j, end_part in enumerate(end_parts):
                                        if end_part.startswith("silence_end:"):
                                            end = float(end_part.split(":")[-1])
                                            duration = end - start
                                            silence_segments.append(
                                                SilenceSegment(
                                                    start=start,
                                                    end=end,
                                                    duration=duration,
                                                )
                                            )
                                    break

            self.logger.info(f"Detected {len(silence_segments)} silence segments")
            return silence_segments

        except Exception as e:
            self.logger.error(f"Error detecting silence: {e}")
            return []

    def remove_silence(
        self,
        input_path: Path,
        output_path: Path,
        min_silence_duration: float = MIN_SILENCE_DURATION,
    ) -> bool:
        """Remove silence from video"""
        try:
            # Use silenceremove filter
            cmd = [
                "ffmpeg",
                "-i",
                str(input_path),
                "-af",
                f"silenceremove=1:0:{min_silence_duration}",
                "-c:v",
                "copy",
                str(output_path),
            ]

            result = subprocess.run(cmd, capture_output=True, timeout=300)

            if result.returncode == 0:
                self.logger.info(f"✅ Removed silence: {output_path}")
                return True
            else:
                self.logger.error(f"Error removing silence: {result.stderr}")
                return False

        except Exception as e:
            self.logger.error(f"Error in remove_silence: {e}")
            return False

    def normalize_audio(self, input_path: Path, output_path: Path) -> bool:
        """Normalize audio to target level"""
        try:
            cmd = [
                "ffmpeg",
                "-i",
                str(input_path),
                "-af",
                f"volume={AUDIO_NORMALIZATION_DB}dB",
                "-c:v",
                "copy",
                str(output_path),
            ]

            result = subprocess.run(cmd, capture_output=True, timeout=300)

            if result.returncode == 0:
                self.logger.info(f"✅ Normalized audio: {output_path}")
                return True
            else:
                self.logger.error(f"Error normalizing audio: {result.stderr}")
                return False

        except Exception as e:
            self.logger.error(f"Error in normalize_audio: {e}")
            return False

    def apply_color_grade(
        self,
        input_path: Path,
        output_path: Path,
        warmth: int = 50,
        contrast: int = 50,
        saturation: int = 50,
    ) -> bool:
        """Apply color grading to video"""
        try:
            # Convert warmth/contrast/saturation (0-100) to filter values
            # Warmth: colortemperature filter
            # Contrast/Saturation: eq filter

            warmth_value = 1000 + (warmth - 50) * 20  # 900-1100K range

            cmd = [
                "ffmpeg",
                "-i",
                str(input_path),
                "-vf",
                f"colortemperature={warmth_value},eq=contrast={contrast/50:.2f}:saturation={saturation/50:.2f}",
                "-c:a",
                "copy",
                str(output_path),
            ]

            result = subprocess.run(cmd, capture_output=True, timeout=300)

            if result.returncode == 0:
                self.logger.info(
                    f"✅ Applied color grading: {output_path} (warmth={warmth})"
                )
                return True
            else:
                self.logger.error(f"Error applying color grading: {result.stderr}")
                return False

        except Exception as e:
            self.logger.error(f"Error in apply_color_grade: {e}")
            return False

    def extract_audio(self, video_path: Path, audio_path: Path) -> bool:
        """Extract audio from video"""
        try:
            cmd = [
                "ffmpeg",
                "-i",
                str(video_path),
                "-q:a",
                "9",
                "-n",
                str(audio_path),
            ]

            result = subprocess.run(cmd, capture_output=True, timeout=120)

            if result.returncode == 0:
                self.logger.info(f"✅ Extracted audio: {audio_path}")
                return True
            else:
                self.logger.error(f"Error extracting audio: {result.stderr}")
                return False

        except Exception as e:
            self.logger.error(f"Error in extract_audio: {e}")
            return False

    def layer_audio(
        self,
        video_path: Path,
        music_path: Path,
        output_path: Path,
        voice_volume_db: float = AUDIO_NORMALIZATION_DB,
        music_volume_db: float = MUSIC_VOLUME_DB,
    ) -> bool:
        """Layer music under voice audio in video"""
        try:
            cmd = [
                "ffmpeg",
                "-i",
                str(video_path),
                "-i",
                str(music_path),
                "-filter_complex",
                f"[0:a]volume={voice_volume_db}dB[a0]; [1:a]volume={music_volume_db}dB[a1]; [a0][a1]amix=inputs=2:duration=first[out]",
                "-map",
                "0:v",
                "-map",
                "[out]",
                "-c:v",
                "copy",
                "-shortest",
                str(output_path),
            ]

            result = subprocess.run(cmd, capture_output=True, timeout=300)

            if result.returncode == 0:
                self.logger.info(f"✅ Layered audio: {output_path}")
                return True
            else:
                self.logger.error(f"Error layering audio: {result.stderr}")
                return False

        except Exception as e:
            self.logger.error(f"Error in layer_audio: {e}")
            return False

    def resize_and_export(
        self,
        input_path: Path,
        output_path: Path,
        platform: str,
    ) -> bool:
        """Resize video for platform and export"""
        if platform not in PLATFORM_SPECS:
            self.logger.error(f"Unknown platform: {platform}")
            return False

        try:
            spec = PLATFORM_SPECS[platform]
            width = spec["width"]
            height = spec["height"]

            cmd = [
                "ffmpeg",
                "-i",
                str(input_path),
                "-vf",
                f"scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2",
                "-c:a",
                "aac",
                "-b:a",
                "128k",
                "-c:v",
                "libx264",
                "-preset",
                "medium",
                "-crf",
                "23",
                str(output_path),
            ]

            result = subprocess.run(cmd, capture_output=True, timeout=600)

            if result.returncode == 0:
                self.logger.info(
                    f"✅ Exported for {platform}: {output_path} ({width}x{height})"
                )
                return True
            else:
                self.logger.error(f"Error exporting for {platform}: {result.stderr}")
                return False

        except Exception as e:
            self.logger.error(f"Error in resize_and_export: {e}")
            return False
