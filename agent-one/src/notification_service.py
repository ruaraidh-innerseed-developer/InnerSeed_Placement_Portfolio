"""Notification Service - Sends notifications when videos are ready"""

import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, List
import os


class NotificationService:
    """Sends notifications via email or other channels"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.email_configured = self._check_email_config()

    def _check_email_config(self) -> bool:
        """Check if email is configured"""
        return all(
            [
                os.getenv("SMTP_SERVER"),
                os.getenv("SMTP_PORT"),
                os.getenv("SENDER_EMAIL"),
                os.getenv("SENDER_PASSWORD"),
                os.getenv("RECIPIENT_EMAIL"),
            ]
        )

    def notify_completion(
        self, video_name: str, output_paths: Dict[str, str], brief_json: Dict
    ) -> None:
        """Send notification when video processing is complete"""
        self.logger.info(f"📧 Sending completion notification for {video_name}...")

        subject = f"✅ Video Ready: {video_name.rsplit('.', 1)[0]}"

        # Build email body
        body = self._build_completion_email(video_name, brief_json, output_paths)

        if self.email_configured:
            self._send_email(subject, body)
        else:
            self.logger.info(f"📝 Would send notification:\n{subject}\n\n{body}")

    def notify_error(self, video_name: str, error_message: str) -> None:
        """Send notification on processing error"""
        self.logger.info(f"📧 Sending error notification for {video_name}...")

        subject = f"❌ Error: {video_name}"
        body = f"""Processing failed for: {video_name}

Error: {error_message}

The video has been moved to the /Agent-One-Errors/ folder.
Please review the logs for more details.

Agent One
"""

        if self.email_configured:
            self._send_email(subject, body)
        else:
            self.logger.info(f"📝 Would send error notification:\n{subject}\n\n{body}")

    def notify_status(self, status_message: str) -> None:
        """Send periodic status notification"""
        self.logger.info(f"📧 Sending status notification...")

        subject = "🤖 Agent One - Status Update"

        if self.email_configured:
            self._send_email(subject, status_message)
        else:
            self.logger.info(f"📝 Status:\n{status_message}")

    def _build_completion_email(
        self, video_name: str, brief_json: Dict, output_paths: Dict[str, str]
    ) -> str:
        """Build the completion email body"""
        video_base = video_name.rsplit(".", 1)[0]

        body = f"""✅ VIDEO PROCESSING COMPLETE

Video: {video_name}
Content Type: {brief_json.get('content_type', 'Unknown')}
Tone: {', '.join(brief_json.get('tone', []))}
Title: {brief_json.get('title', 'Untitled')}

PLATFORM VERSIONS READY:
"""

        platforms = brief_json.get("platform_targets", [])
        for platform in platforms:
            body += f"\n✓ {platform.upper()}"
            if platform in output_paths:
                body += f" (ID: {output_paths[platform]})"

        body += f"""

NEXT STEPS:
1. Open Google Drive: /Agent-One-Outbox/{video_base}/
2. Review each platform version
3. Check the summary file for captions and details
4. Download videos or share directly to platforms
5. Delete from outbox after posting

CAPTIONS GENERATED:
- Instagram: Optimized for feeds and Reels
- TikTok: Short, pattern-interrupt style
- YouTube: Long-form with SEO keywords
- LinkedIn: Professional, thought leadership

Need to make changes? Upload a new version with an updated brief to /Agent-One-Inbox/

---
Agent One - Autonomous Video Processing
"""

        return body

    def _send_email(self, subject: str, body: str) -> bool:
        """Send email notification"""
        try:
            smtp_server = os.getenv("SMTP_SERVER")
            smtp_port = int(os.getenv("SMTP_PORT", 587))
            sender_email = os.getenv("SENDER_EMAIL")
            sender_password = os.getenv("SENDER_PASSWORD")
            recipient_email = os.getenv("RECIPIENT_EMAIL")

            # Create message
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = recipient_email
            message["Subject"] = subject
            message.attach(MIMEText(body, "plain"))

            # Send email
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(message)

            self.logger.info(f"✅ Email sent to {recipient_email}")
            return True

        except Exception as e:
            self.logger.error(f"❌ Failed to send email: {e}")
            return False
