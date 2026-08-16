"""Caption Generator - Generates platform-specific captions using Claude"""

import json
import logging
from typing import Dict, Any
from anthropic import Anthropic


class CaptionGenerator:
    """Generates platform-specific captions using Claude"""

    def __init__(self, client: Anthropic):
        self.client = client
        self.logger = logging.getLogger(__name__)

    def generate_captions(
        self, transcript: str, brief_json: Dict[str, Any], timestamps: Dict[str, str]
    ) -> Dict[str, str]:
        """
        Generate 4 platform-specific captions from transcript

        Args:
            transcript: Full transcription of the video
            brief_json: Parsed brief with context
            timestamps: Optional timestamp data

        Returns:
            Dictionary with captions for each platform
        """
        self.logger.info("✍️  Generating platform-specific captions...")

        prompt = f"""You are a social media expert. Generate captions for 4 different platforms based on this video.

TRANSCRIPT:
{transcript}

VIDEO CONTEXT:
- Content type: {brief_json.get('content_type', 'general')}
- Tone: {', '.join(brief_json.get('tone', []))}
- Title: {brief_json.get('title', 'Untitled')}
- Description: {brief_json.get('description', '')}

Generate ONLY valid JSON (no markdown, no explanation) with these 4 captions:

{{
  "instagram": "<150-250 words, conversational, emojis, hook first, call-to-action>",
  "tiktok": "<50-100 words, pattern interrupt, trending angle, short punchy>",
  "youtube": "<200+ words, educational, SEO keywords, detailed, searchable>",
  "linkedin": "<150-200 words, professional tone, thought leadership, no casual emojis>"
}}

Make each caption:
- Authentic to the content
- Optimized for the platform's style
- Compelling and engaging
- Include relevant hashtags where appropriate"""

        try:
            response = self.client.messages.create(
                model="claude-opus-5",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}],
            )

            response_text = response.content[0].text

            # Parse JSON from response
            captions = json.loads(response_text)

            self.logger.info("✅ Captions generated for all platforms")
            return captions

        except json.JSONDecodeError as e:
            self.logger.error(f"❌ Failed to parse captions JSON: {e}")
            return self._get_default_captions(brief_json)
        except Exception as e:
            self.logger.error(f"❌ Error generating captions: {e}")
            return self._get_default_captions(brief_json)

    def _get_default_captions(self, brief_json: Dict[str, Any]) -> Dict[str, str]:
        """Return default captions if generation fails"""
        title = brief_json.get("title", "Check out this video")
        description = brief_json.get("description", "Professional video content")

        return {
            "instagram": f"{title}\n\n{description}\n\nCheck out the full video! 🎬 #video #content",
            "tiktok": f"{title}\n\n{description} 🎯",
            "youtube": f"{title}\n\n{description}\n\nEnjoy this professionally edited video!",
            "linkedin": f"{title}\n\n{description}\n\nWatch the full video for more insights.",
        }
