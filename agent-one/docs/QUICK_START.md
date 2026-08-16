# Agent One - Quick Start Guide

Get Agent One running in 15 minutes!

## TL;DR

```bash
# 1. Setup
cp .env.example .env
# Edit .env with your API keys and folder IDs

# 2. Test
python src/agent.py --mode once

# 3. Run
python src/agent.py --mode scheduled
```

## Detailed Steps

### 1. Get Your API Keys (5 min)

You need 4 API keys:

1. **Claude** - [https://console.anthropic.com](https://console.anthropic.com)
   - Click "API Keys" → "Create Key"
   - Copy key (starts with `sk-ant-`)

2. **OpenAI Whisper** - [https://platform.openai.com](https://platform.openai.com)
   - Go to "API Keys" → "Create New Secret Key"
   - Copy key (starts with `sk-`)

3. **Descript** - [https://www.descript.com](https://www.descript.com)
   - Settings → API → Copy API key

4. **Pixabay** - [https://pixabay.com](https://pixabay.com)
   - Settings → API → Copy key

### 2. Setup Google Drive (5 min)

#### Create folders in Google Drive:
- `Agent-One-Inbox` → get folder ID from URL
- `Agent-One-Outbox` → get folder ID from URL
- `Agent-One-Logs` → get folder ID from URL
- `Agent-One-Errors` → get folder ID from URL

#### Get service account:
1. [Google Cloud Console](https://console.cloud.google.com)
2. Create project "Agent One"
3. Enable "Google Drive API"
4. Create Service Account → Download JSON key
5. Share all 4 folders with service account email (editor permission)

### 3. Configure Agent One (3 min)

```bash
# Copy example config
cp .env.example .env

# Edit .env
nano .env
```

Fill in:
```
CLAUDE_API_KEY=your-key-here
WHISPER_API_KEY=your-key-here
DESCRIPT_API_KEY=your-key-here
PIXABAY_API_KEY=your-key-here
GOOGLE_DRIVE_OAUTH_JSON='{"type": "service_account", ...}'
AGENT_ONE_INBOX_FOLDER_ID=your-id-here
AGENT_ONE_OUTBOX_FOLDER_ID=your-id-here
AGENT_ONE_LOGS_FOLDER_ID=your-id-here
AGENT_ONE_ERRORS_FOLDER_ID=your-id-here
```

### 4. Install & Test (2 min)

```bash
# Install dependencies
pip install -r requirements.txt

# Test with one video
python src/agent.py --mode once
```

Check logs:
```bash
tail -f logs/agent_one.log
```

### 5. Deploy (optional)

```bash
# Run continuously (every 30 minutes)
python src/agent.py --mode scheduled
```

Or add to crontab:
```bash
crontab -e
# Add: */30 * * * * cd /path/to/agent-one && python src/agent.py --mode once
```

## Now You're Ready!

### Upload a test video:
1. Create a video file: `test.mp4`
2. Create brief file: `test_brief.txt`
   ```
   This is a test video.
   Remove pauses.
   Add ambient music.
   Warm color grade.
   Target Instagram.
   ```
3. Upload both to `/Agent-One-Inbox/`

### Run Agent:
```bash
python src/agent.py --mode once
```

### Check results:
- Look in `/Agent-One-Outbox/test/`
- Find: `test_instagram.mp4`, `test_summary.txt`

### View logs:
```bash
cat logs/agent_one.log
```

## Common Commands

```bash
# Run once (for testing)
python src/agent.py --mode once

# Run continuously
python src/agent.py --mode scheduled

# Run with custom interval (60 minutes)
python src/agent.py --mode scheduled --interval 60

# View logs
tail -f logs/agent_one.log

# View today's activity
cat logs/processing_log_$(date +%Y-%m-%d).txt

# View completed videos
cat logs/completed_videos.json
```

## Troubleshooting

### "FFmpeg not found"
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg

# Windows
choco install ffmpeg
```

### "API key not recognized"
- Check you have the correct key (no spaces)
- Verify key is in .env, not as environment variable
- Check keys haven't expired

### "Google Drive authentication failed"
- Verify service account JSON is valid
- Check service account email has access to folders
- Try re-sharing folders with service account

### "No videos to process"
- Check brief file name: must be `{video-name}_brief.txt`
- Both video and brief must be in same folder
- Check `/Agent-One-Inbox/` has both files

## What Happens Next

Agent One will:
1. ✅ Check inbox every 30 minutes
2. ✅ Download your video + brief
3. ✅ Parse instructions (Claude)
4. ✅ Edit video intelligently
5. ✅ Transcribe audio (Whisper)
6. ✅ Generate captions (Claude, 4 platforms)
7. ✅ Add music (Pixabay)
8. ✅ Apply color grading
9. ✅ Export for 4 platforms
10. ✅ Upload to `/Agent-One-Outbox/`

Each video takes **35-50 minutes** to fully process.

## Next Steps

- Read [SETUP.md](./SETUP.md) for detailed configuration
- Read [API_USAGE.md](./API_USAGE.md) for API details
- Check [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) for known issues

## You're All Set! 🚀

Agent One is now ready to process your videos 24/7!

Any questions? Check the logs in `/agent-one/logs/` for detailed information about what's happening.
