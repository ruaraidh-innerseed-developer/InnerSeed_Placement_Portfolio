"""Agent One - Autonomous Video Processing Agent"""

import logging
import time
import signal
import sys
from datetime import datetime
from pathlib import Path
import os

from config.constants import (
    PROCESSING_SCHEDULE_MINUTES,
    INBOX_FOLDER_ID,
    OUTBOX_FOLDER_ID,
    LOGS_FOLDER_ID,
    ERRORS_FOLDER_ID,
    LOGS_DIR,
)
from video_processor import VideoProcessor


def setup_logging():
    """Configure logging"""
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.FileHandler(LOGS_DIR / "agent_one.log"),
            logging.StreamHandler(),
        ],
    )
    return logging.getLogger(__name__)


class AgentOne:
    """Main Agent One orchestrator"""

    def __init__(self):
        self.logger = setup_logging()
        self.processor = VideoProcessor()
        self.running = True

        # Register signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

        self.logger.info("=" * 60)
        self.logger.info("🚀 Agent One Starting")
        self.logger.info("=" * 60)

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        self.logger.info("Received shutdown signal, gracefully shutting down...")
        self.running = False
        sys.exit(0)

    def validate_config(self) -> bool:
        """Validate required configuration"""
        required_vars = {
            "INBOX_FOLDER_ID": INBOX_FOLDER_ID,
            "OUTBOX_FOLDER_ID": OUTBOX_FOLDER_ID,
            "LOGS_FOLDER_ID": LOGS_FOLDER_ID,
        }

        missing = []
        for var_name, var_value in required_vars.items():
            if not var_value:
                missing.append(var_name)

        if missing:
            self.logger.error(f"Missing required configuration: {', '.join(missing)}")
            self.logger.info(
                "Set these environment variables:\n"
                "  export AGENT_ONE_INBOX_FOLDER_ID=...\n"
                "  export AGENT_ONE_OUTBOX_FOLDER_ID=...\n"
                "  export AGENT_ONE_LOGS_FOLDER_ID=...\n"
                "  export AGENT_ONE_ERRORS_FOLDER_ID=... (optional)"
            )
            return False

        self.logger.info("✅ Configuration validated")
        return True

    def run_once(self) -> bool:
        """Run a single processing cycle"""
        self.logger.info(f"\n{'=' * 60}")
        self.logger.info(f"📅 Processing cycle: {datetime.now().isoformat()}")
        self.logger.info(f"{'=' * 60}")

        try:
            result = self.processor.process_video(
                inbox_folder_id=INBOX_FOLDER_ID,
                outbox_folder_id=OUTBOX_FOLDER_ID,
                logs_folder_id=LOGS_FOLDER_ID,
                errors_folder_id=ERRORS_FOLDER_ID,
            )

            if result["status"] == "success":
                self.logger.info(
                    f"✅ Processed {result['videos_processed']} video(s) "
                    f"in {result['total_time_minutes']:.1f} minutes"
                )
                return True
            elif result["status"] == "no_videos":
                self.logger.info("No new videos to process")
                return False
            else:
                self.logger.error(f"Processing failed: {result.get('error', 'Unknown error')}")
                return False

        except Exception as e:
            self.logger.error(f"Error in processing cycle: {e}")
            return False

    def run_scheduled(self):
        """Run agent on a schedule (default: every 30 minutes)"""
        self.logger.info(
            f"Agent running in scheduled mode (every {PROCESSING_SCHEDULE_MINUTES} minutes)"
        )
        self.logger.info("Press Ctrl+C to stop")

        cycle_count = 0

        while self.running:
            try:
                cycle_count += 1
                self.logger.info(f"\nCycle #{cycle_count}")
                self.run_once()

                # Wait for next cycle
                self.logger.info(
                    f"⏰ Next cycle in {PROCESSING_SCHEDULE_MINUTES} minutes "
                    f"({datetime.now().isoformat()})"
                )
                time.sleep(PROCESSING_SCHEDULE_MINUTES * 60)

            except KeyboardInterrupt:
                self.logger.info("Keyboard interrupt received")
                break
            except Exception as e:
                self.logger.error(f"Unexpected error in scheduled loop: {e}")
                time.sleep(60)  # Wait 1 minute before retry

        self.logger.info("Agent shutting down")

    def run_once_mode(self):
        """Run agent once and exit (useful for testing/cron)"""
        self.logger.info("Agent running in single-cycle mode")
        self.run_once()
        self.logger.info("Agent completed")


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="Agent One - Video Processing Agent")
    parser.add_argument(
        "--mode",
        choices=["scheduled", "once"],
        default="scheduled",
        help="Run mode (default: scheduled)",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=PROCESSING_SCHEDULE_MINUTES,
        help=f"Processing interval in minutes (default: {PROCESSING_SCHEDULE_MINUTES})",
    )

    args = parser.parse_args()

    agent = AgentOne()

    if not agent.validate_config():
        sys.exit(1)

    try:
        if args.mode == "once":
            agent.run_once_mode()
        else:  # scheduled
            agent.run_scheduled()

    except KeyboardInterrupt:
        pass
    except Exception as e:
        agent.logger.error(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
