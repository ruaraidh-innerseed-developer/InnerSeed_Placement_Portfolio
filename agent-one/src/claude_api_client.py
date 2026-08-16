"""Claude API Client for brief parsing and caption generation"""

import json
import logging
from typing import Dict, Optional, Any
import anthropic

from config.constants import CLAUDE_API_KEY, CAPTION_SPECS


class ClaudeAPIClient:
    """Handles Claude API interactions for brief parsing and captions"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)
        self.logger.info("✅ Initialized Claude API client")

    def parse_brief(self, brief_text: str) -> Optional[Dict[str, Any]]:
        """Parse voice brief instructions into structured JSON"""
        try:
            prompt = f"""Parse the following voice brief instructions into structured JSON format.

Voice Brief:
{brief_text}

Return a JSON object with these fields:
- content_type: one of [meditation, vlog, speech, interview]
- duration_target: target duration in seconds (integer)
- tone: list of adjectives describing the desired tone
- edits: list of editing instructions (e.g., "remove_pauses", "remove_ums")
- music: object with {{style, volume_db, intensity}} (or null if no music)
- color_grade: object with {{warmth (0-100), contrast (0-100), saturation (0-100), preset}}
- title: suggested title for the video
- description: suggested description
- platform_targets: list of platforms [instagram, tiktok, youtube, linkedin]

Return ONLY valid JSON, no additional text."""

            message = self.client.messages.create(
                model="claude-opus-4-1",
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}],
            )

            # Extract JSON from response
            response_text = message.content[0].text.strip()

            # Remove markdown code blocks if present
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]

            brief_json = json.loads(response_text.strip())

            self.logger.info(f"✅ Parsed brief: {brief_json.get('title', 'Untitled')}")
            return brief_json

        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse Claude response as JSON: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Error parsing brief with Claude: {e}")
            return None

    def generate_captions(
        self, transcript: str, brief_json: Dict[str, Any]
    ) -> Optional[Dict[str, str]]:
        """Generate platform-specific captions from transcript and brief"""
        try:
            platforms = brief_json.get("platform_targets", [])
            if not platforms:
                platforms = ["instagram", "tiktok", "youtube", "linkedin"]

            prompt = f"""Generate platform-specific social media captions based on this content.

Transcript:
{transcript}

Content Brief:
- Title: {brief_json.get('title', 'Untitled')}
- Tone: {', '.join(brief_json.get('tone', []))}
- Description: {brief_json.get('description', '')}

Generate captions for these platforms: {', '.join(platforms)}

For each platform, follow these guidelines:
- Instagram: 150-250 words, use emojis, start with a compelling hook, casual tone
- TikTok: 50-100 words, pattern interrupt style, trending angle, use emojis
- YouTube: 200+ words, educational focus, include SEO keywords, informative tone
- LinkedIn: 150-200 words, professional tone, no emojis, business-focused

Return a JSON object with keys: instagram, tiktok, youtube, linkedin
Only include captions for the requested platforms.
Return ONLY valid JSON, no additional text."""

            message = self.client.messages.create(
                model="claude-opus-4-1",
                max_tokens=2048,
                messages=[{"role": "user", "content": prompt}],
            )

            response_text = message.content[0].text.strip()

            # Remove markdown code blocks if present
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]

            captions = json.loads(response_text.strip())

            self.logger.info(f"✅ Generated captions for {len(captions)} platforms")
            return captions

        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse captions response as JSON: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Error generating captions with Claude: {e}")
            return None

    def estimate_captions_from_video(
        self, visual_description: str, brief_json: Dict[str, Any]
    ) -> Optional[Dict[str, str]]:
        """Fallback: Generate captions from visual description when transcript unavailable"""
        try:
            prompt = f"""Generate platform-specific captions based on this video description.

Visual Description:
{visual_description}

Content Brief:
- Title: {brief_json.get('title', 'Untitled')}
- Tone: {', '.join(brief_json.get('tone', []))}
- Type: {brief_json.get('content_type', 'unknown')}

Generate captions for Instagram, TikTok, YouTube, and LinkedIn.
Follow platform guidelines for each.

Return ONLY valid JSON with keys: instagram, tiktok, youtube, linkedin"""

            message = self.client.messages.create(
                model="claude-opus-4-1",
                max_tokens=2048,
                messages=[{"role": "user", "content": prompt}],
            )

            response_text = message.content[0].text.strip()

            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]

            captions = json.loads(response_text.strip())

            self.logger.info(
                "✅ Generated estimated captions from visual description"
            )
            return captions

        except Exception as e:
            self.logger.error(f"Error generating estimated captions: {e}")
            return None

    def validate_brief_json(self, brief_json: Dict[str, Any]) -> bool:
        """Validate parsed brief JSON has all required fields"""
        required_fields = [
            "content_type",
            "duration_target",
            "tone",
            "platform_targets",
        ]

        for field in required_fields:
            if field not in brief_json:
                self.logger.warning(f"Missing required field in brief: {field}")
                return False

        return True

    def get_caption_confidence_score(self, brief_json: Dict[str, Any]) -> float:
        """Get confidence score for brief parsing (0-1)"""
        # Simple heuristic: more detailed briefs = higher confidence
        fields_present = sum(
            1
            for field in [
                "tone",
                "edits",
                "music",
                "color_grade",
                "title",
                "description",
            ]
            if field in brief_json and brief_json[field]
        )
        return min(1.0, fields_present / 6.0)
