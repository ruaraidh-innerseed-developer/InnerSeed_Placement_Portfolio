"""Main Video Processor - Orchestrates the entire processing pipeline"""

import logging
import time
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any
import json
import shutil

from config.constants import TEMP_DIR, CONTENT_TYPES
from state_manager import StateManager
from google_drive_client import GoogleDriveClient
from ffmpeg_handler import FFmpegHandler
from claude_api_client import ClaudeAPIClient
from external_apis import WhisperClient, DescriptClient, PixabayMusicClient


class VideoProcessor:
    """Main orchestrator for video processing pipeline"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.state = StateManager()
        self.drive = GoogleDriveClient()
        self.ffmpeg = FFmpegHandler()
        self.claude = ClaudeAPIClient()
        self.whisper = WhisperClient()
        self.descript = DescriptClient()
        self.pixabay = PixabayMusicClient()

    def process_video(
        self,
        inbox_folder_id: str,
        outbox_folder_id: str,
        logs_folder_id: str,
        errors_folder_id: str,
    ) -> Dict[str, Any]:
        """Main processing pipeline"""
        start_time = datetime.now()

        try:
            # Step 1: Monitor & Detect
            self.logger.info("🔍 Checking Inbox for new videos...")
            video_brief_pairs = self.drive.find_video_and_brief(inbox_folder_id)

            if not video_brief_pairs:
                self.logger.info("No new videos to process")
                return {"status": "no_videos"}

            results = []

            for video_file, brief_file in video_brief_pairs:
                if brief_file is None:
                    self.logger.warning(
                        f"Video {video_file['name']} has no brief file, skipping"
                    )
                    continue

                # Check if already processed
                if self.state.is_video_processed(video_file["name"]):
                    self.logger.info(f"Video {video_file['name']} already processed")
                    continue

                result = self._process_single_video(
                    video_file,
                    brief_file,
                    inbox_folder_id,
                    outbox_folder_id,
                    errors_folder_id,
                )
                results.append(result)

            processing_time = (datetime.now() - start_time).total_seconds() / 60
            self.logger.info(f"Processing complete. Time: {processing_time:.1f} minutes")

            return {
                "status": "complete",
                "videos_processed": len(results),
                "results": results,
                "total_time_minutes": processing_time,
            }

        except Exception as e:
            self.logger.error(f"Error in main processing loop: {e}")
            return {"status": "error", "error": str(e)}

    def _process_single_video(
        self,
        video_file: Dict,
        brief_file: Dict,
        inbox_folder_id: str,
        outbox_folder_id: str,
        errors_folder_id: str,
    ) -> Dict[str, Any]:
        """Process a single video through the pipeline"""
        video_name = video_file["name"]
        job_id = f"{video_file['id']}_{int(time.time())}"

        # Create job entry
        job = self.state.create_job(video_file["id"], video_name, brief_file["name"])

        # Create temporary directory for this video
        temp_video_dir = TEMP_DIR / job_id
        temp_video_dir.mkdir(parents=True, exist_ok=True)

        try:
            # Step 2: Download & Analyze
            self.logger.info(f"📥 Processing: {video_name}")
            self.state.update_job(job_id, status="downloading")

            video_path = temp_video_dir / video_file["name"]
            brief_path = temp_video_dir / brief_file["name"]

            self.drive.download_file(video_file["id"], video_path)
            self.drive.download_file(brief_file["id"], brief_path)

            # Get video metadata
            metadata = self.ffmpeg.get_video_metadata(video_path)
            if not metadata:
                raise Exception("Failed to get video metadata")

            # Analyze silence
            silence_segments = self.ffmpeg.detect_silence(video_path)
            self.state.update_job(
                job_id,
                status="analyzing",
                metadata={"duration": metadata.duration, "silence_segments": len(silence_segments)},
            )

            # Step 3: Parse Brief
            self.logger.info(f"📋 Parsing brief: {brief_file['name']}")
            with open(brief_path, "r") as f:
                brief_text = f.read()

            brief_json = self.claude.parse_brief(brief_text)
            if not brief_json:
                raise Exception("Failed to parse brief")

            self.state.update_job(
                job_id,
                status="parsed",
                content_type=brief_json.get("content_type"),
                platforms=brief_json.get("platform_targets", []),
            )

            # Step 4: Intelligent Editing
            self.logger.info("✂️ Editing video...")
            self.state.update_job(job_id, status="editing")

            edited_video_path = temp_video_dir / "edited_video.mp4"
            self._edit_video(
                video_path,
                edited_video_path,
                brief_json,
                silence_segments,
                metadata,
            )

            # Step 5: Transcribe
            self.logger.info("🎤 Transcribing audio...")
            self.state.update_job(job_id, status="transcribing")

            audio_path = temp_video_dir / "audio.wav"
            self.ffmpeg.extract_audio(edited_video_path, audio_path)

            transcript_result = self.whisper.transcribe(audio_path)
            if not transcript_result:
                self.logger.warning("Whisper transcription failed, using fallback")
                transcript = "Video content"
            else:
                transcript = transcript_result.get("text", "")

            # Step 6: Generate Captions
            self.logger.info("📝 Generating captions...")
            self.state.update_job(job_id, status="captioning")

            captions = self.claude.generate_captions(transcript, brief_json)
            if not captions:
                raise Exception("Failed to generate captions")

            # Step 7: Layer Music
            self.logger.info("🎵 Layering music...")
            self.state.update_job(job_id, status="music")

            music_video_path = edited_video_path
            if brief_json.get("music"):
                music_video_path = temp_video_dir / "video_with_music.mp4"
                if not self._add_music(
                    edited_video_path, music_video_path, brief_json["music"]
                ):
                    self.logger.warning("Music layering failed, continuing without music")
                    music_video_path = edited_video_path

            # Step 8: Descript Finishing (simplified - would integrate real API)
            self.logger.info("🎬 Finishing video...")
            self.state.update_job(job_id, status="finishing")

            platforms = brief_json.get("platform_targets", [])
            output_paths = self._export_platforms(
                music_video_path, temp_video_dir, platforms, brief_json
            )

            if not output_paths:
                raise Exception("Failed to export videos")

            # Step 9: Upload to Outbox
            self.logger.info("📤 Uploading to Outbox...")
            self.state.update_job(job_id, status="uploading")

            outbox_paths = self._upload_to_outbox(
                job_id,
                video_name,
                output_paths,
                temp_video_dir,
                brief_json,
                outbox_folder_id,
            )

            # Mark job complete
            processing_time = (datetime.now() - job.created_at).total_seconds() / 60
            self.state.complete_job(job_id, outbox_paths, processing_time)

            self.logger.info(f"✅ Video processing complete: {video_name}")

            # Cleanup temp directory
            shutil.rmtree(temp_video_dir, ignore_errors=True)

            return {
                "video": video_name,
                "status": "success",
                "platforms": platforms,
                "processing_time_minutes": processing_time,
                "output_paths": outbox_paths,
            }

        except Exception as e:
            self.logger.error(f"Error processing video {video_name}: {e}")
            self.state.fail_job(job_id, str(e))

            # Move video to errors folder
            if errors_folder_id:
                self.drive.move_file(video_file["id"], errors_folder_id)

            # Cleanup
            shutil.rmtree(temp_video_dir, ignore_errors=True)

            return {
                "video": video_name,
                "status": "error",
                "error": str(e),
            }

    def _edit_video(
        self,
        input_path: Path,
        output_path: Path,
        brief_json: Dict,
        silence_segments: list,
        metadata,
    ) -> bool:
        """Apply intelligent editing based on content type and brief"""
        try:
            content_type = brief_json.get("content_type", "vlog")
            config = CONTENT_TYPES.get(content_type, CONTENT_TYPES["vlog"])

            # Apply color grading if specified
            temp_path = output_path.parent / "temp_edit.mp4"
            color_grade = brief_json.get("color_grade", {})

            if color_grade:
                self.ffmpeg.apply_color_grade(
                    input_path,
                    temp_path,
                    warmth=color_grade.get("warmth", 50),
                    contrast=color_grade.get("contrast", 50),
                    saturation=color_grade.get("saturation", 50),
                )
                input_path = temp_path

            # Normalize audio
            self.ffmpeg.normalize_audio(input_path, output_path)

            return True

        except Exception as e:
            self.logger.error(f"Error editing video: {e}")
            return False

    def _add_music(
        self, video_path: Path, output_path: Path, music_spec: Dict
    ) -> bool:
        """Add music to video"""
        try:
            # Search for music
            music_style = music_spec.get("style", "ambient")
            music_tracks = self.pixabay.search_music(f"{music_style} music", limit=1)

            if not music_tracks:
                self.logger.warning("No music tracks found")
                return False

            # Download music
            best_track = music_tracks[0]
            music_path = video_path.parent / f"music_{best_track['id']}.mp3"

            if not self.pixabay.download_music(best_track["download_url"], music_path):
                return False

            # Layer music
            return self.ffmpeg.layer_audio(
                video_path,
                music_path,
                output_path,
                music_volume_db=music_spec.get("volume_db", -12),
            )

        except Exception as e:
            self.logger.error(f"Error adding music: {e}")
            return False

    def _export_platforms(
        self, video_path: Path, temp_dir: Path, platforms: list, brief_json: Dict
    ) -> Dict[str, str]:
        """Export video for multiple platforms"""
        output_paths = {}

        try:
            for platform in platforms:
                output_file = temp_dir / f"output_{platform}.mp4"
                if self.ffmpeg.resize_and_export(video_path, output_file, platform):
                    output_paths[platform] = str(output_file)
                else:
                    self.logger.warning(f"Failed to export for {platform}")

            return output_paths

        except Exception as e:
            self.logger.error(f"Error exporting platforms: {e}")
            return {}

    def _upload_to_outbox(
        self,
        job_id: str,
        video_name: str,
        output_paths: Dict,
        temp_dir: Path,
        brief_json: Dict,
        outbox_folder_id: str,
    ) -> Dict[str, str]:
        """Upload finished videos to outbox"""
        try:
            outbox_paths = {}

            # Create outbox subfolder
            video_base_name = video_name.rsplit(".", 1)[0]
            subfolder_id = self.drive.create_folder(video_base_name, outbox_folder_id)

            if not subfolder_id:
                self.logger.error("Failed to create outbox subfolder")
                return {}

            # Upload video files
            for platform, file_path in output_paths.items():
                file_name = f"{video_base_name}_{platform}.mp4"
                file_id = self.drive.upload_file(Path(file_path), subfolder_id, file_name)
                if file_id:
                    outbox_paths[platform] = file_id

            # Create summary file
            summary = self._create_summary(video_name, brief_json, job_id)
            summary_path = temp_dir / "summary.txt"
            with open(summary_path, "w") as f:
                f.write(summary)

            self.drive.upload_file(summary_path, subfolder_id, f"{video_base_name}_summary.txt")

            return outbox_paths

        except Exception as e:
            self.logger.error(f"Error uploading to outbox: {e}")
            return {}

    def _create_summary(
        self, video_name: str, brief_json: Dict, job_id: str
    ) -> str:
        """Create processing summary file"""
        summary = f"""Video Processing Summary
========================

Video: {video_name}
Job ID: {job_id}
Processed: {datetime.now().isoformat()}

Content Details
---------------
Type: {brief_json.get('content_type', 'Unknown')}
Title: {brief_json.get('title', 'Untitled')}
Description: {brief_json.get('description', 'N/A')}
Duration Target: {brief_json.get('duration_target', 'N/A')}s

Tone: {', '.join(brief_json.get('tone', []))}

Editing
-------
Edits Applied: {', '.join(brief_json.get('edits', ['none']))}

Color Grade:
  Warmth: {brief_json.get('color_grade', {}).get('warmth', 'N/A')}
  Contrast: {brief_json.get('color_grade', {}).get('contrast', 'N/A')}
  Saturation: {brief_json.get('color_grade', {}).get('saturation', 'N/A')}

Music:
  Style: {brief_json.get('music', {}).get('style', 'None')}
  Volume: {brief_json.get('music', {}).get('volume_db', 'N/A')}dB

Platforms
---------
Exported for: {', '.join(brief_json.get('platform_targets', ['All']))}

Status: ✅ Ready for Review
"""

        return summary
