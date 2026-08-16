"""
Claude Console Agent for Agent One
Main orchestrator - uses Claude API for decision-making and orchestration
Monitors Google Drive every 30 minutes and processes videos end-to-end
"""

import asyncio
import json
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List

from anthropic import Anthropic

from config.constants import (
    CLAUDE_API_KEY,
    INBOX_FOLDER_ID,
    OUTBOX_FOLDER_ID,
    LOGS_FOLDER_ID,
    ERRORS_FOLDER_ID,
    PROCESSING_SCHEDULE_MINUTES,
)
from src.state_manager import StateManager
from src.google_drive_client import GoogleDriveClient
from src.video_processor import VideoProcessor
from src.brief_parser import BriefParser
from src.caption_generator import CaptionGenerator
from src.notification_service import NotificationService


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler("agent-one/logs/agent_one.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


class ClaudeAgentOne:
    """
    Claude Console Agent for Agent One
    Autonomous video processing agent that runs 24/7 on a 30-minute schedule
    """

    def __init__(self):
        """Initialize Agent One with all necessary clients and services"""
        self.logger = logger
        self.logger.info("🚀 Initializing Claude Agent One...")

        # Initialize Anthropic client
        self.client = Anthropic(api_key=CLAUDE_API_KEY)

        # Initialize services
        self.state_manager = StateManager()
        self.google_drive = GoogleDriveClient()
        self.video_processor = VideoProcessor()
        self.brief_parser = BriefParser(self.client)
        self.caption_generator = CaptionGenerator(self.client)
        self.notification_service = NotificationService()

        # Store conversation history for multi-turn interactions
        self.conversation_history = []

        self.logger.info("✅ Claude Agent One initialized successfully")

    def _get_agent_system_prompt(self) -> str:
        """Get the system prompt for Claude Agent One"""
        return """You are Agent One, an autonomous video processing agent.

Your mission:
1. Monitor Google Drive /Agent-One-Inbox/ for new video + brief pairs
2. Process videos end-to-end through 9 steps
3. Generate 4 platform-specific versions (Instagram, TikTok, YouTube, LinkedIn)
4. Move finished videos to /Agent-One-Outbox/
5. Maintain detailed logs of all operations
6. Run autonomously 24/7 on a 30-minute schedule

You have access to:
- Google Drive API (read/write)
- FFmpeg for video analysis and editing
- Claude API for decision-making and caption generation
- Whisper API for transcription
- Descript API for professional finishing
- Pixabay API for royalty-free music
- State persistence (remember what you've processed)

Processing Pipeline:
1. Monitor inbox for new videos
2. Download & analyze with FFmpeg
3. Parse brief with Claude
4. Apply intelligent editing (content-type aware)
5. Transcribe audio with Whisper
6. Generate platform-specific captions with Claude
7. Layer music from Pixabay
8. Apply professional finishing with Descript
9. Export 4 platform versions to outbox

Guidelines:
- Always check if video was already processed (avoid duplicates)
- Handle errors gracefully with retries and fallbacks
- Log every step with timestamp
- Preserve quality while optimizing for each platform
- Remember completed videos to prevent re-processing

You are professional, systematic, and reliable. Every operation is logged."""

    def analyze_inbox(self) -> List[tuple]:
        """Use Claude to analyze inbox and determine next action"""
        self.logger.info("📍 Analyzing inbox with Claude...")

        # Get list of videos in inbox
        videos_and_briefs = self.google_drive.find_video_and_brief(INBOX_FOLDER_ID)

        if not videos_and_briefs:
            self.logger.info("📭 No videos found in inbox")
            return []

        # Filter out already processed videos
        unprocessed = []
        for video, brief in videos_and_briefs:
            if not self.state_manager.is_video_processed(video["name"]):
                if brief:  # Only process if brief exists
                    unprocessed.append((video, brief))
                else:
                    self.logger.warning(
                        f"⚠️  Video {video['name']} found but no brief file"
                    )

        self.logger.info(f"📹 Found {len(unprocessed)} unprocessed video(s)")

        # Send to Claude for decision
        if unprocessed:
            video_list = [
                f"- {video['name']} (brief: {brief['name']})"
                for video, brief in unprocessed
            ]
            analysis_prompt = f"""I found these unprocessed videos in the inbox:
{chr(10).join(video_list)}

Which video should I process first?
Respond with JUST the video filename and I'll start processing."""

            self.conversation_history.append(
                {"role": "user", "content": analysis_prompt}
            )

            response = self.client.messages.create(
                model="claude-opus-5",
                max_tokens=500,
                system=self._get_agent_system_prompt(),
                messages=self.conversation_history,
            )

            claude_response = response.content[0].text
            self.conversation_history.append(
                {"role": "assistant", "content": claude_response}
            )

            self.logger.info(f"🧠 Claude decision: {claude_response}")

        return unprocessed

    def process_video(self, video: Dict, brief: Dict) -> bool:
        """Process a single video through the complete pipeline"""
        self.logger.info(f"🎬 Starting processing for {video['name']}")

        # Create job
        job = self.state_manager.create_job(video["id"], video["name"], brief["name"])
        job_id = video["id"]

        try:
            # Step 1: Download & Analyze
            self.logger.info("📥 Step 1: Downloading & analyzing video...")
            self.state_manager.update_job(job_id, status="processing")

            video_path = Path("agent-one/temp") / video["name"]
            brief_path = Path("agent-one/temp") / brief["name"]

            if not self.google_drive.download_file(video["id"], video_path):
                raise Exception("Failed to download video")
            if not self.google_drive.download_file(brief["id"], brief_path):
                raise Exception("Failed to download brief")

            analysis = self.video_processor.analyze_video(video_path)
            self.logger.info(f"✅ Analysis complete: {analysis}")
            self.state_manager.update_job(job_id, metadata={"analysis": analysis})

            # Step 2: Parse Brief
            self.logger.info("📋 Step 2: Parsing brief with Claude...")
            brief_text = brief_path.read_text()
            brief_json = self.brief_parser.parse_brief(brief_text, analysis)
            self.logger.info(f"✅ Brief parsed: {brief_json}")
            self.state_manager.update_job(
                job_id,
                content_type=brief_json.get("content_type"),
                platforms=brief_json.get("platform_targets", []),
            )

            # Step 3: Intelligent Editing
            self.logger.info("✂️  Step 3: Applying intelligent editing...")
            edited_video = self.video_processor.edit_video(
                video_path, brief_json, analysis
            )
            self.logger.info(f"✅ Video edited: {edited_video}")

            # Step 4: Transcribe
            self.logger.info("🎙️  Step 4: Transcribing with Whisper...")
            transcript, timestamps = self.video_processor.transcribe_video(edited_video)
            self.logger.info(f"✅ Transcription complete: {len(transcript)} words")

            # Step 5: Generate Captions
            self.logger.info("✍️  Step 5: Generating platform-specific captions...")
            captions = self.caption_generator.generate_captions(
                transcript, brief_json, timestamps
            )
            self.logger.info(f"✅ Captions generated for all platforms")

            # Step 6: Layer Music
            self.logger.info("🎵 Step 6: Layering music...")
            video_with_music = self.video_processor.layer_music(edited_video, brief_json)
            self.logger.info(f"✅ Music layered: {video_with_music}")

            # Step 7: Descript Finishing
            self.logger.info("🎨 Step 7: Applying professional finishing with Descript...")
            finished_videos = self.video_processor.apply_descript_finishing(
                video_with_music, captions, brief_json
            )
            self.logger.info(f"✅ Professional finishing complete")

            # Step 8: Upload to Outbox
            self.logger.info("📤 Step 8: Uploading to outbox...")
            output_paths = self._upload_to_outbox(
                finished_videos, captions, video["name"], brief_json
            )
            self.logger.info(f"✅ Uploaded to outbox: {output_paths}")

            # Mark job as completed
            processing_time = (datetime.now().timestamp() - job.created_at.__sizeof__()) / 60
            self.state_manager.complete_job(job_id, output_paths, processing_time)

            # Notify user
            self.notification_service.notify_completion(
                video["name"], output_paths, brief_json
            )

            self.logger.info(f"✅ Video processing complete: {video['name']}")
            return True

        except Exception as e:
            self.logger.error(f"❌ Error processing video: {e}")
            self.state_manager.fail_job(job_id, str(e))

            # Move to errors folder
            if ERRORS_FOLDER_ID:
                self.google_drive.move_file(video["id"], ERRORS_FOLDER_ID)

            return False

    def _upload_to_outbox(
        self,
        finished_videos: Dict[str, Path],
        captions: Dict[str, str],
        video_name: str,
        brief_json: Dict,
    ) -> Dict[str, str]:
        """Upload finished videos and summary to outbox"""
        output_paths = {}

        # Create folder for this video
        video_folder_name = video_name.rsplit(".", 1)[0]
        outbox_folder = self.google_drive.create_folder(
            video_folder_name, OUTBOX_FOLDER_ID
        )

        if not outbox_folder:
            self.logger.error("Failed to create outbox folder")
            return {}

        # Upload each platform version
        for platform, video_path in finished_videos.items():
            file_name = f"{video_folder_name}_{platform}.mp4"
            file_id = self.google_drive.upload_file(video_path, outbox_folder, file_name)
            if file_id:
                output_paths[platform] = file_id

        # Create and upload summary file
        summary_content = self._create_summary(
            video_name, brief_json, captions, finished_videos
        )
        summary_path = Path("agent-one/temp") / f"{video_folder_name}_summary.txt"
        summary_path.write_text(summary_content)

        summary_id = self.google_drive.upload_file(
            summary_path, outbox_folder, f"{video_folder_name}_summary.txt"
        )
        if summary_id:
            output_paths["summary"] = summary_id

        return output_paths

    def _create_summary(
        self,
        video_name: str,
        brief_json: Dict,
        captions: Dict[str, str],
        finished_videos: Dict[str, Path],
    ) -> str:
        """Create processing summary file"""
        summary = f"""=== VIDEO PROCESSING SUMMARY ===
Video: {video_name}
Processed: {datetime.now().isoformat()}

CONTENT TYPE
{brief_json.get('content_type', 'Unknown')}

TONE
{', '.join(brief_json.get('tone', []))}

PLATFORMS
{', '.join(brief_json.get('platform_targets', []))}

CAPTIONS
--- Instagram ---
{captions.get('instagram', 'N/A')}

--- TikTok ---
{captions.get('tiktok', 'N/A')}

--- YouTube ---
{captions.get('youtube', 'N/A')}

--- LinkedIn ---
{captions.get('linkedin', 'N/A')}

STATUS
✅ Ready for review and posting

NEXT STEPS
1. Review each platform version
2. Verify captions are accurate
3. Check color grading and music balance
4. Post to desired platforms
"""
        return summary

    def run_once(self) -> None:
        """Run agent once (process one cycle)"""
        self.logger.info("=" * 60)
        self.logger.info("🤖 Claude Agent One - Processing Cycle")
        self.logger.info("=" * 60)

        try:
            # Analyze inbox
            unprocessed = self.analyze_inbox()

            if not unprocessed:
                self.logger.info("✅ No videos to process. Sleeping...")
                return

            # Process first video
            video, brief = unprocessed[0]
            self.process_video(video, brief)

        except Exception as e:
            self.logger.error(f"❌ Critical error in processing cycle: {e}")
            self.state_manager.log_activity(f"❌ Critical error: {e}")

    def run_scheduled(self, interval_minutes: int = PROCESSING_SCHEDULE_MINUTES) -> None:
        """Run agent continuously on a schedule"""
        self.logger.info(f"🔄 Starting scheduled agent (every {interval_minutes} min)")

        try:
            while True:
                self.run_once()
                self.logger.info(f"⏰ Next check in {interval_minutes} minutes...")
                time.sleep(interval_minutes * 60)

        except KeyboardInterrupt:
            self.logger.info("🛑 Agent stopped by user")
        except Exception as e:
            self.logger.error(f"❌ Fatal error: {e}")

    def run_daemon(self) -> None:
        """Run as a daemon service"""
        self.logger.info("👹 Starting Agent One as daemon...")
        self.run_scheduled()


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="Claude Agent One - Video Processing Agent")
    parser.add_argument(
        "--mode",
        choices=["once", "scheduled", "daemon"],
        default="scheduled",
        help="Run mode: once (single cycle), scheduled (loop), daemon (background)",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=PROCESSING_SCHEDULE_MINUTES,
        help="Schedule interval in minutes (default: 30)",
    )

    args = parser.parse_args()

    # Initialize agent
    agent = ClaudeAgentOne()

    # Run in requested mode
    if args.mode == "once":
        agent.run_once()
    elif args.mode == "scheduled":
        agent.run_scheduled(args.interval)
    elif args.mode == "daemon":
        agent.run_daemon()


if __name__ == "__main__":
    main()
