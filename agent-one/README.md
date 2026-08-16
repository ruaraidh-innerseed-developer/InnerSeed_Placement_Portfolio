# Agent One - Autonomous Video Processing Agent

An autonomous Claude agent that processes videos end-to-end for multi-platform social media distribution. Upload a video + brief, and Agent One handles editing, captioning, music layering, and exports 4 platform-optimized versions.

## Features

✅ **Fully Autonomous** - Runs 24/7 on a schedule
✅ **Google Drive Integration** - Monitors inbox, uploads to outbox
✅ **Intelligent Editing** - Content-aware video processing (meditation, vlog, speech, interview)
✅ **Multi-Platform Export** - Instagram, TikTok, YouTube, LinkedIn
✅ **AI-Powered Captions** - Platform-specific caption generation via Claude
✅ **Audio Processing** - Silence detection, music layering, normalization
✅ **Persistent State** - Remembers completed videos, prevents re-processing
✅ **Error Handling** - Graceful failures with retry logic and error logging

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                  AGENT ONE                          │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌─────────────────────────────────────────────┐   │
│  │  1. Monitor Inbox (Google Drive)            │   │
│  └──────────────────┬──────────────────────────┘   │
│                     ▼                               │
│  ┌─────────────────────────────────────────────┐   │
│  │  2. Download & Analyze (FFmpeg)             │   │
│  └──────────────────┬──────────────────────────┘   │
│                     ▼                               │
│  ┌─────────────────────────────────────────────┐   │
│  │  3. Parse Brief (Claude API)                │   │
│  └──────────────────┬──────────────────────────┘   │
│                     ▼                               │
│  ┌─────────────────────────────────────────────┐   │
│  │  4. Intelligent Editing (FFmpeg)            │   │
│  └──────────────────┬──────────────────────────┘   │
│                     ▼                               │
│  ┌─────────────────────────────────────────────┐   │
│  │  5. Transcribe Audio (Whisper API)          │   │
│  └──────────────────┬──────────────────────────┘   │
│                     ▼                               │
│  ┌─────────────────────────────────────────────┐   │
│  │  6. Generate Captions (Claude API)          │   │
│  └──────────────────┬──────────────────────────┘   │
│                     ▼                               │
│  ┌─────────────────────────────────────────────┐   │
│  │  7. Add Music (Pixabay API + FFmpeg)        │   │
│  └──────────────────┬──────────────────────────┘   │
│                     ▼                               │
│  ┌─────────────────────────────────────────────┐   │
│  │  8. Apply Color Grading & Finishing (FFmpeg)│   │
│  └──────────────────┬──────────────────────────┘   │
│                     ▼                               │
│  ┌─────────────────────────────────────────────┐   │
│  │  9. Export to Platforms (FFmpeg)            │   │
│  └──────────────────┬──────────────────────────┘   │
│                     ▼                               │
│  ┌─────────────────────────────────────────────┐   │
│  │  10. Upload to Outbox (Google Drive)        │   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## Setup & Installation

### Prerequisites

- Python 3.9+
- FFmpeg + FFprobe installed
- Google Drive access with service account
- API keys for: Claude, OpenAI Whisper, Descript, Pixabay Music

### 1. Install Dependencies

```bash
cd agent-one
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the project root:

```bash
# API Keys
export CLAUDE_API_KEY="sk-ant-..."
export WHISPER_API_KEY="sk-..."
export DESCRIPT_API_KEY="..."
export PIXABAY_API_KEY="..."

# Google Drive Service Account (JSON string)
export GOOGLE_DRIVE_OAUTH_JSON='{"type": "service_account", ...}'

# Google Drive Folder IDs
export AGENT_ONE_INBOX_FOLDER_ID="1abc..."
export AGENT_ONE_OUTBOX_FOLDER_ID="2def..."
export AGENT_ONE_LOGS_FOLDER_ID="3ghi..."
export AGENT_ONE_ERRORS_FOLDER_ID="4jkl..."
```

### 3. Get Google Drive Folder IDs

In Google Drive:
1. Create folders: `Agent-One-Inbox`, `Agent-One-Outbox`, `Agent-One-Logs`, `Agent-One-Errors`
2. Share them with your service account email
3. Get folder IDs from the URL: `https://drive.google.com/drive/folders/{FOLDER_ID}`

### 4. Setup Google Drive Service Account

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project
3. Enable Google Drive API
4. Create a service account
5. Generate a JSON key
6. Set `GOOGLE_DRIVE_OAUTH_JSON` to the JSON content

## Usage

### Run Agent (Scheduled Mode)

```bash
cd agent-one/src
python agent.py --mode scheduled --interval 30
```

This will:
- Check inbox every 30 minutes
- Process any new videos with brief files
- Upload finished videos to outbox
- Maintain state to prevent re-processing

### Run Agent Once (Testing/Cron)

```bash
cd agent-one/src
python agent.py --mode once
```

Useful for:
- Testing the setup
- Running via cron job
- Manual processing cycles

## Voice Brief System

User uploads to Google Drive `/Agent-One-Inbox/`:

```
meditation_v1.mp4
meditation_v1_brief.txt
```

**Example brief.txt:**
```
This is a meditation. Cut pauses and ums. 
Add calm ambient music underneath. 
Keep it 5 minutes. Make it dreamy. 
Warm color grade. Target Instagram Reels.
```

Agent parses this into:
```json
{
  "content_type": "breathwork_meditation",
  "duration_target": 300,
  "tone": ["dreamy", "peaceful"],
  "edits": ["remove_pauses", "remove_ums"],
  "music": {"style": "ambient", "volume_db": -12},
  "color_grade": {"warmth": 75, "contrast": 50},
  "platform_targets": ["instagram"]
}
```

## Platform Specifications

### Instagram
- **Resolution:** 1080x1350 (4:5 vertical)
- **Caption Style:** Casual, emojis, 150-250 words
- **Use Case:** Reels, feed posts

### TikTok
- **Resolution:** 1080x1920 (9:16 full vertical)
- **Caption Style:** Pattern interrupt, trending angle, 50-100 words
- **Use Case:** TikTok native format

### YouTube
- **Resolution:** 1080x1920 (9:16 YouTube Shorts)
- **Caption Style:** Educational, SEO keywords, 200+ words
- **Use Case:** YouTube Shorts, long-form

### LinkedIn
- **Resolution:** 1200x628 (16:9 landscape)
- **Caption Style:** Professional, no emojis, 150-200 words
- **Use Case:** Professional content, thought leadership

## Output Structure

Agent creates this in `/Agent-One-Outbox/`:

```
/Agent-One-Outbox/
└─ meditation_v1/
   ├─ meditation_v1_instagram.mp4
   ├─ meditation_v1_tiktok.mp4
   ├─ meditation_v1_youtube.mp4
   ├─ meditation_v1_linkedin.mp4
   └─ meditation_v1_summary.txt
      ├─ Processing time: 47 min
      ├─ Content: Breathwork meditation
      ├─ Edits applied: remove_pauses, remove_ums
      ├─ Music: Ambient style, -12dB volume
      ├─ Color grade: Warmth 75%, Contrast 50%
      └─ Captions: [4 platform variants]
```

## Logging

All activity is logged to `/agent-one/logs/`:

```
agent_one.log           # Main agent log
processing_log_2026-08-16.txt  # Daily activity log
completed_videos.json   # List of processed videos
current_jobs.json       # Jobs in progress
```

## Project Structure

```
agent-one/
├── src/
│   ├── __init__.py
│   ├── agent.py                 # Main agent orchestrator
│   ├── video_processor.py        # Processing pipeline
│   ├── state_manager.py          # State persistence
│   ├── google_drive_client.py    # Google Drive API
│   ├── ffmpeg_handler.py         # Video editing
│   ├── claude_api_client.py      # Claude AI integration
│   └── external_apis.py          # Whisper, Descript, Pixabay
├── config/
│   └── constants.py              # Configuration
├── tests/
│   ├── test_ffmpeg.py
│   ├── test_claude_api.py
│   └── test_state_manager.py
├── docs/
│   ├── SETUP.md
│   ├── API_USAGE.md
│   └── TROUBLESHOOTING.md
├── requirements.txt
├── setup.py
└── README.md
```

## Configuration

Edit `config/constants.py` to customize:

```python
# Processing frequency
PROCESSING_SCHEDULE_MINUTES = 30

# FFmpeg settings
SILENCE_THRESHOLD_DB = -50
MIN_SILENCE_DURATION = 0.5
AUDIO_NORMALIZATION_DB = -3
MUSIC_VOLUME_DB = -12

# Content-specific settings
CONTENT_TYPES = {
    "meditation": {...},
    "vlog": {...},
    "speech": {...},
    "interview": {...},
}

# Platform specifications
PLATFORM_SPECS = {...}
CAPTION_SPECS = {...}
```

## Error Handling

Agent handles failures gracefully:

```
FFmpeg fails          → Move to /Errors, notify user, retry after 1h
Whisper fails         → Retry 3x, fallback to estimated captions
Descript fails        → Retry with backoff, fallback to FFmpeg export
Music unavailable     → Skip music, process without it
Brief parse fails     → Move to /Errors with reason
```

All errors logged with timestamp and reason.

## Testing

Run tests with:

```bash
cd agent-one
python -m pytest tests/ -v
```

Manual test:
1. Create test video + brief in `/Agent-One-Inbox/`
2. Run: `python src/agent.py --mode once`
3. Check `/Agent-One-Outbox/` for results
4. Verify `/Agent-One-Logs/` for processing details

## Performance

- **Per video:** 35-50 minutes (depending on length and complexity)
- **Processing breakdown:**
  - Download & analyze: 2 min
  - Parse brief: 1 min
  - Edit video: 10-15 min
  - Transcribe: 3 min
  - Generate captions: 3 min
  - Add music: 5 min
  - Color grading: 5 min
  - Export (4 platforms): 10-15 min
  - Upload to Drive: 2 min

## Cost

Monthly cost breakdown:
- Claude API: Included (captions, brief parsing)
- Whisper API: ~$10 (30 videos × $0.33/min average)
- Descript API: ~$35 (existing subscription)
- **Total: ~$45-50/month**

Per-video cost: ~$1.50-$1.70

## Known Limitations

- Descript API integration is simplified (production version needs full API implementation)
- Pixabay Music API limited to available tracks (no guaranteed perfect match)
- FFmpeg processing times vary based on video length and resolution
- Whisper transcription quality depends on audio clarity

## Future Enhancements

- [ ] Real-time progress notifications
- [ ] Advanced color grading profiles
- [ ] Multi-language support
- [ ] A/B testing for captions
- [ ] Analytics integration
- [ ] Voice command support
- [ ] Custom watermarks/branding
- [ ] Batch video processing

## Troubleshooting

### "FFmpeg not found"
```bash
# Install FFmpeg
# Ubuntu/Debian:
sudo apt-get install ffmpeg

# macOS:
brew install ffmpeg

# Windows:
choco install ffmpeg
```

### "Google Drive authentication failed"
- Verify service account has Drive API enabled
- Check `GOOGLE_DRIVE_OAUTH_JSON` format (must be valid JSON)
- Ensure service account email has access to Drive folders

### "No modules named X"
```bash
pip install -r requirements.txt --upgrade
```

### Videos not processing
1. Check `/Agent-One-Logs/agent_one.log` for errors
2. Verify brief files are named `[video-name]_brief.txt`
3. Ensure brief file is in same folder as video
4. Check folder IDs in environment variables

## Support

For issues or questions:
1. Check logs in `/agent-one/logs/`
2. Review troubleshooting section above
3. Test with `--mode once` to debug
4. Check API keys and permissions

## License

MIT License - See LICENSE file for details

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## Roadmap

### Phase 1 (Complete)
- [x] Core video processing pipeline
- [x] Google Drive integration
- [x] Claude API integration
- [x] FFmpeg handlers
- [x] State management
- [x] Error handling

### Phase 2 (In Progress)
- [ ] Full Descript API integration
- [ ] Advanced color grading profiles
- [ ] Real-time notifications
- [ ] Web dashboard

### Phase 3 (Planned)
- [ ] Mobile app integration
- [ ] Analytics dashboard
- [ ] A/B testing framework
- [ ] Multi-user support

---

**Built with Claude** - An autonomous agent for content creators, by content creators.
