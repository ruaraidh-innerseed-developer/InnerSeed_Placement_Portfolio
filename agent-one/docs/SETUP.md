# Agent One - Complete Setup Guide

This guide walks you through setting up Agent One step-by-step.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Google Drive Setup](#google-drive-setup)
3. [API Keys Configuration](#api-keys-configuration)
4. [Environment Setup](#environment-setup)
5. [Testing](#testing)
6. [Deployment](#deployment)

---

## Prerequisites

Before starting, ensure you have:

- **Python 3.9+** installed
- **FFmpeg** installed (for video processing)
- **Google Account** (for Google Drive)
- API keys from:
  - Claude (Anthropic)
  - OpenAI Whisper
  - Descript
  - Pixabay

### Install FFmpeg

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install ffmpeg
ffmpeg -version  # Verify installation
```

**macOS:**
```bash
brew install ffmpeg
ffmpeg -version  # Verify installation
```

**Windows:**
```bash
choco install ffmpeg
ffmpeg -version  # Verify installation
```

---

## Google Drive Setup

### Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Click "Select a Project" → "NEW PROJECT"
3. Name it "Agent One"
4. Click "CREATE"
5. Wait for the project to be created

### Step 2: Enable Google Drive API

1. In Cloud Console, search for "Google Drive API"
2. Click on "Google Drive API"
3. Click "ENABLE"
4. Wait for it to enable

### Step 3: Create Service Account

1. In Cloud Console, go to "APIs & Services" → "Credentials"
2. Click "CREATE CREDENTIALS" → "Service Account"
3. Fill in:
   - Service account name: "agent-one"
   - Service account ID: (auto-filled)
   - Click "CREATE AND CONTINUE"
4. In "Grant this service account access to project":
   - Click "Continue" (we'll set permissions differently)
5. Click "CREATE KEY" → "JSON"
   - A JSON file will download (save this!)
6. Click "DONE"

### Step 4: Create Google Drive Folders

1. Go to [Google Drive](https://drive.google.com)
2. Create 4 folders:
   - `Agent-One-Inbox` - where you upload videos
   - `Agent-One-Outbox` - where finished videos are saved
   - `Agent-One-Logs` - where logs are stored
   - `Agent-One-Errors` - where failed videos are moved

3. For each folder:
   - Right-click → "Share"
   - Share with the service account email (from the JSON key file, looks like: `agent-one@project-id.iam.gserviceaccount.com`)
   - Give it "Editor" permissions
   - Uncheck "Notify people"
   - Click "Share"

### Step 5: Get Folder IDs

For each of the 4 folders:
1. Open the folder in Google Drive
2. Copy the folder ID from the URL bar
   - Example URL: `https://drive.google.com/drive/folders/1abc123def456xyz`
   - Folder ID: `1abc123def456xyz`
3. Save all 4 folder IDs

---

## API Keys Configuration

### Claude API Key

1. Go to [Anthropic Console](https://console.anthropic.com)
2. Sign up or log in
3. Go to "API Keys"
4. Click "Create Key"
5. Copy the key (starts with `sk-ant-`)
6. Save safely

### OpenAI Whisper API Key

1. Go to [OpenAI Platform](https://platform.openai.com)
2. Sign up or log in
3. Go to "API Keys" → "Create New Secret Key"
4. Copy the key (starts with `sk-`)
5. Save safely

### Descript API Key

1. Go to [Descript](https://www.descript.com)
2. Sign up or log in
3. Go to "Settings" → "API"
4. Generate an API key
5. Copy and save safely

### Pixabay Music API Key

1. Go to [Pixabay](https://pixabay.com)
2. Sign up or log in
3. Go to "Settings" → "API"
4. Copy your API key
5. Save safely

---

## Environment Setup

### Step 1: Clone/Setup Project

```bash
cd agent-one
pip install -r requirements.txt
```

### Step 2: Create .env File

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and fill in:

```bash
# API Keys
CLAUDE_API_KEY=sk-ant-your-key-here
WHISPER_API_KEY=sk-your-key-here
DESCRIPT_API_KEY=your-descript-key-here
PIXABAY_API_KEY=your-pixabay-key-here

# Google Drive Service Account JSON
GOOGLE_DRIVE_OAUTH_JSON='{"type": "service_account", ...}'
# (Paste the entire content of your JSON key file)

# Google Drive Folder IDs
AGENT_ONE_INBOX_FOLDER_ID=your-inbox-folder-id
AGENT_ONE_OUTBOX_FOLDER_ID=your-outbox-folder-id
AGENT_ONE_LOGS_FOLDER_ID=your-logs-folder-id
AGENT_ONE_ERRORS_FOLDER_ID=your-errors-folder-id
```

### Step 3: Verify Environment

```bash
# Test that all environment variables are set
python -c "
import os
required = ['CLAUDE_API_KEY', 'WHISPER_API_KEY', 'DESCRIPT_API_KEY', 
            'PIXABAY_API_KEY', 'GOOGLE_DRIVE_OAUTH_JSON',
            'AGENT_ONE_INBOX_FOLDER_ID', 'AGENT_ONE_OUTBOX_FOLDER_ID',
            'AGENT_ONE_LOGS_FOLDER_ID', 'AGENT_ONE_ERRORS_FOLDER_ID']
for var in required:
    if not os.getenv(var):
        print(f'Missing: {var}')
    else:
        print(f'✅ {var}')
"
```

---

## Testing

### Test 1: FFmpeg

```bash
ffmpeg -version
ffprobe -version
```

Should show version info for both.

### Test 2: Google Drive Connection

```bash
cd src
python -c "
import sys
sys.path.insert(0, '..')
from google_drive_client import GoogleDriveClient
client = GoogleDriveClient()
print('✅ Google Drive authentication successful')
"
```

### Test 3: API Keys

```bash
cd src
python -c "
import sys
sys.path.insert(0, '..')
from claude_api_client import ClaudeAPIClient
client = ClaudeAPIClient()
print('✅ Claude API authentication successful')
"
```

### Test 4: Single Processing Cycle

1. Create a test video and brief in your `/Agent-One-Inbox/` folder:

   Test video: `test_video.mp4` (any video file)
   
   Test brief: `test_video_brief.txt` with content:
   ```
   This is a test meditation video.
   Cut any pauses.
   Add ambient music.
   Warm color grade.
   Target Instagram only.
   ```

2. Run Agent One once:
   ```bash
   cd src
   python agent.py --mode once
   ```

3. Watch the logs:
   ```bash
   tail -f ../logs/agent_one.log
   ```

4. Check results in `/Agent-One-Outbox/`:
   - Should see `test_video/` folder
   - Should contain: `test_video_instagram.mp4`, `test_video_summary.txt`

### Test 5: Check Logs

```bash
# View main log
cat logs/agent_one.log

# View daily processing log
cat logs/processing_log_$(date +%Y-%m-%d).txt

# View completed videos
cat logs/completed_videos.json
```

---

## Deployment

### Option 1: Scheduled (Recommended)

Run Agent One continuously on a schedule:

```bash
cd agent-one/src
python agent.py --mode scheduled --interval 30
```

This will:
- Check inbox every 30 minutes
- Process any new videos
- Continue running indefinitely

### Option 2: Cron Job

Set up a cron job to run Agent One periodically:

```bash
# Open crontab editor
crontab -e

# Add this line to run every 30 minutes:
*/30 * * * * cd /path/to/agent-one && python src/agent.py --mode once

# Or run every hour:
0 * * * * cd /path/to/agent-one && python src/agent.py --mode once

# Or run every 6 hours:
0 */6 * * * cd /path/to/agent-one && python src/agent.py --mode once
```

### Option 3: Systemd Service (Linux)

Create a systemd service file:

```bash
sudo nano /etc/systemd/system/agent-one.service
```

Add:
```ini
[Unit]
Description=Agent One - Autonomous Video Processor
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/path/to/agent-one
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/python src/agent.py --mode scheduled
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl daemon-reload
sudo systemctl enable agent-one
sudo systemctl start agent-one
sudo systemctl status agent-one
```

### Option 4: Docker (Advanced)

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

# Install FFmpeg
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Create logs directory
RUN mkdir -p logs temp cache

# Run agent
CMD ["python", "src/agent.py", "--mode", "scheduled"]
```

Build and run:
```bash
docker build -t agent-one .
docker run -d \
  -e CLAUDE_API_KEY=... \
  -e WHISPER_API_KEY=... \
  -e DESCRIPT_API_KEY=... \
  -e PIXABAY_API_KEY=... \
  -e GOOGLE_DRIVE_OAUTH_JSON='...' \
  -e AGENT_ONE_INBOX_FOLDER_ID=... \
  -e AGENT_ONE_OUTBOX_FOLDER_ID=... \
  -e AGENT_ONE_LOGS_FOLDER_ID=... \
  --name agent-one \
  agent-one
```

---

## Monitoring

### Check Agent Status

```bash
# View active logs
tail -f logs/agent_one.log

# View today's processing
tail -f logs/processing_log_$(date +%Y-%m-%d).txt

# View completed videos
cat logs/completed_videos.json | jq .

# View current jobs
cat logs/current_jobs.json | jq .
```

### Monitor Google Drive

- Check `/Agent-One-Inbox/` for new videos
- Check `/Agent-One-Outbox/` for finished videos
- Check `/Agent-One-Logs/` for processing logs
- Check `/Agent-One-Errors/` for failed videos

---

## Troubleshooting

### Issue: "FFmpeg not found"
```bash
# Reinstall FFmpeg
sudo apt-get install ffmpeg  # Linux
brew install ffmpeg          # macOS
choco install ffmpeg         # Windows
```

### Issue: "Google Drive authentication failed"
- Verify service account JSON is valid
- Check service account email has access to all 4 folders
- Verify GOOGLE_DRIVE_OAUTH_JSON is complete JSON string

### Issue: "API key invalid"
- Check you're using the correct API key for each service
- Verify keys haven't expired
- Check for trailing spaces in .env file

### Issue: Videos not processing
1. Check brief file name: must be `{video-name}_brief.txt`
2. Check both files are in same folder
3. Run `python agent.py --mode once` to debug
4. Check logs for error messages

### Issue: "No space left on device"
- Clean up `/agent-one/temp/` directory
- Check disk space: `df -h`
- Delete old videos after confirming they're in outbox

---

## Next Steps

1. ✅ Setup complete!
2. 📹 Upload test videos to `/Agent-One-Inbox/`
3. 📝 Create brief files for each video
4. ▶️ Run Agent One: `python src/agent.py --mode once`
5. 📤 Monitor logs and check `/Agent-One-Outbox/`
6. 🚀 Deploy to production (cron, systemd, or Docker)

---

## Support

If you encounter issues:
1. Check the logs in `/agent-one/logs/`
2. Review error messages carefully
3. Verify all API keys are set
4. Check FFmpeg is installed: `ffmpeg -version`
5. Test Google Drive access manually
6. Review TROUBLESHOOTING.md for known issues

---

**Agent One is ready to process videos!** 🎬
