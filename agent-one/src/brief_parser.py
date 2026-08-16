"""Brief Parser - Parses voice instructions into structured JSON"""

import json
import logging
from typing import Dict, Any
from anthropic import Anthropic


class BriefParser:
    """Parses brief text files into structured JSON using Claude"""

    def __init__(self, client: Anthropic):
        self.client = client
        self.logger = logging.getLogger(__name__)

    def parse_brief(self, brief_text: str, video_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse voice brief (text instructions) into structured JSON

        Args:
            brief_text: The brief text file content
            video_analysis: Analysis results from FFmpeg (duration, resolution, etc.)

        Returns:
            Structured JSON with all processing parameters
        """
        self.logger.info("🔍 Parsing brief with Claude...")

        prompt = f"""You are a professional video editor's assistant. Parse these video instructions into structured JSON.

BRIEF TEXT:
{brief_text}

VIDEO ANALYSIS:
Duration: {video_analysis.get('duration', 'unknown')} seconds
Resolution: {video_analysis.get('resolution', 'unknown')}
Aspect ratio: {video_analysis.get('aspect_ratio', 'unknown')}

Parse into this JSON structure (return ONLY valid JSON, no markdown, no explanation):
{{
  "content_type": "meditation|vlog|speech|interview|other",
  "duration_target": <seconds or null>,
  "tone": [<list of tone adjectives>],
  "edits": [<list of editing actions: remove_pauses, remove_ums, remove_filler, cut_silence, tighten_pacing, preserve_breathing>],
  "music": {{
    "include": true|false,
    "style": "ambient|energetic|cinematic|upbeat|calm|epic|other",
    "volume_db": <-12 to 0>,
    "intensity": "low|medium|high"
  }},
  "color_grade": {{
    "warmth": <0-100>,
    "contrast": <0-100>,
    "saturation": <0-100>,
    "preset": "warm_spiritual|cool_professional|vibrant_energetic|cinematic|natural|other"
  }},
  "title": "<generated title>",
  "description": "<generated description>",
  "platform_targets": [<list of: instagram, tiktok, youtube, linkedin>]
}}"""

        try:
            response = self.client.messages.create(
                model="claude-opus-5",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}],
            )

            response_text = response.content[0].text

            # Parse JSON from response
            brief_json = json.loads(response_text)

            self.logger.info(f"✅ Brief parsed successfully")
            return brief_json

        except json.JSONDecodeError as e:
            self.logger.error(f"❌ Failed to parse JSON response: {e}")
            # Return default structure
            return self._get_default_brief()
        except Exception as e:
            self.logger.error(f"❌ Error parsing brief: {e}")
            return self._get_default_brief()

    def _get_default_brief(self) -> Dict[str, Any]:
        """Return default brief structure if parsing fails"""
        return {
            "content_type": "vlog",
            "duration_target": None,
            "tone": ["professional"],
            "edits": ["remove_pauses", "remove_filler"],
            "music": {
                "include": True,
                "style": "energetic",
                "volume_db": -12,
                "intensity": "medium",
            },
            "color_grade": {
                "warmth": 50,
                "contrast": 50,
                "saturation": 75,
                "preset": "natural",
            },
            "title": "Untitled",
            "description": "Video processed by Agent One",
            "platform_targets": ["instagram", "tiktok", "youtube", "linkedin"],
        }
