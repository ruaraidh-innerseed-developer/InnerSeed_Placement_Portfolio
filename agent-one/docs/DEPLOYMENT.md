# Agent One - Deployment Guide

## Overview

Claude Agent One is an autonomous video processing agent that runs 24/7 and processes videos from Google Drive every 30 minutes.

**Build Time:** 1-2 weeks  
**Cost:** ~$50/month (APIs)  
**Processing Time:** 35-50 min per video  
**Automation:** 100% autonomous

---

## System Requirements

### Hardware
- **CPU:** 2+ cores recommended
- **RAM:** 4GB minimum, 8GB recommended
- **Disk:** 50GB+ for temporary processing
- **Network:** Stable internet connection

### Software
- **Python:** 3.9+
- **FFmpeg:** 4.4+ (required for video processing)
- **Docker:** (optional, for containerized deployment)

### OS Support
- Linux (Ubuntu 20.04+, Debian, CentOS)
- macOS (with Homebrew FFmpeg)
- Windows (WSL2 recommended)

---

## Pre-Deployment Checklist

### 1. API Keys Setup

You need credentials for:

- **Claude API** - For captions & brief parsing
  - Get from: https://console.anthropic.com
  
- **Google Drive API** - For inbox/outbox monitoring
  - Create service account: https://console.cloud.google.com
  - Download JSON key file
  
- **OpenAI Whisper API** - For transcription
  - Get from: https://platform.openai.com/api-keys
  
- **Descript API** - For professional finishing
  - Get from: https://www.descript.com/developers
  
- **Pixabay Music API** - For background music
  - Get from: https://pixabay.com/api/docs/

### 2. Google Drive Setup

Create these folders in Google Drive:

```
/Agent-One-Inbox/      ← Upload videos + briefs here
/Agent-One-Outbox/     ← Agent puts finished videos here
/Agent-One-Logs/       ← Agent stores processing logs
/Agent-One-Errors/     ← Failed videos go here
```

Get folder IDs from share links:
- Go to each folder
- Click "Share" → copy link
- Folder ID is: `https://drive.google.com/drive/folders/FOLDER_ID_HERE`

### 3. Email Notifications (Optional)

If you want email alerts when videos are ready:

- Gmail: Generate app password
  - Settings → Security → App passwords
- Other providers: Use SMTP credentials

---

## Deployment Methods

### Method 1: Systemd Service (Recommended for Linux)

Best for: Production servers, AWS EC2, Linode, DigitalOcean

#### Setup

```bash
# 1. Clone repository
git clone <repo> agent-one
cd agent-one

# 2. Install dependencies
sudo apt-get install ffmpeg python3-pip
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
nano .env  # Edit with your API keys and folder IDs

# 4. Run deployment script
chmod +x deploy.sh
sudo ./deploy.sh
# Choose option 1 for systemd
```

#### Commands

```bash
# Start service
sudo systemctl start agent-one

# Auto-start on reboot
sudo systemctl enable agent-one

# Check status
sudo systemctl status agent-one

# View live logs
sudo journalctl -u agent-one -f

# Stop service
sudo systemctl stop agent-one
```

#### Service File Location
```
/etc/systemd/system/agent-one.service
```

---

### Method 2: Docker (Recommended for Portability)

Best for: Any OS, cloud platforms, containerized infrastructure

#### Setup

```bash
# 1. Clone repository
git clone <repo> agent-one
cd agent-one

# 2. Configure environment
cp .env.example .env
nano .env  # Edit with your API keys

# 3. Build Docker image
docker build -t agent-one:latest .

# 4. Run container
docker run -d \
  --name agent-one \
  --env-file .env \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/temp:/app/temp \
  -v $(pwd)/cache:/app/cache \
  agent-one:latest
```

#### Commands

```bash
# View logs
docker logs -f agent-one

# Check status
docker ps | grep agent-one

# Stop container
docker stop agent-one

# Start container
docker start agent-one

# Remove container
docker rm agent-one
```

#### Docker Compose (Optional)

Create `docker-compose.yml`:

```yaml
version: '3.8'
services:
  agent-one:
    build: .
    container_name: agent-one
    env_file: .env
    volumes:
      - ./logs:/app/logs
      - ./temp:/app/temp
      - ./cache:/app/cache
    restart: always
```

Run:
```bash
docker-compose up -d
docker-compose logs -f
```

---

### Method 3: Cron Job (Simple, Linux Only)

Best for: Simple setups, shared hosting

#### Setup

```bash
# 1. Install and configure
git clone <repo> agent-one
cd agent-one
pip install -r requirements.txt
cp .env.example .env
nano .env  # Configure

# 2. Add cron job
crontab -e

# Add this line to run every 30 minutes:
*/30 * * * * cd /path/to/agent-one && python -m src.claude_agent --mode once >> logs/cron.log 2>&1

# Save and exit (Ctrl+X, then Y, then Enter in nano)
```

#### Monitor

```bash
# View logs
tail -f agent-one/logs/cron.log

# List cron jobs
crontab -l

# Edit cron jobs
crontab -e
```

---

### Method 4: Manual/Development

Best for: Testing, development, learning

#### Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure
cp .env.example .env
nano .env

# 3. Run single cycle
python -m src.claude_agent --mode once

# Or run continuously
python -m src.claude_agent --mode scheduled --interval 30
```

---

## Configuration

### Environment Variables

Edit `.env` file:

```bash
# Required - API Keys
CLAUDE_API_KEY=sk-ant-...
GOOGLE_DRIVE_OAUTH_JSON={"type":"service_account",...}
WHISPER_API_KEY=sk-...
DESCRIPT_API_KEY=...
PIXABAY_API_KEY=...

# Required - Google Drive Folder IDs
AGENT_ONE_INBOX_FOLDER_ID=1a2b3c...
AGENT_ONE_OUTBOX_FOLDER_ID=2b3c4d...
AGENT_ONE_LOGS_FOLDER_ID=3c4d5e...
AGENT_ONE_ERRORS_FOLDER_ID=4d5e6f...

# Optional - Email Notifications
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=app-password
RECIPIENT_EMAIL=recipient@example.com

# Optional - Processing Configuration
PROCESSING_SCHEDULE_MINUTES=30
MAX_RETRIES=3
```

---

## Testing & Verification

### 1. Check Installation

```bash
# Verify FFmpeg
ffmpeg -version

# Verify Python packages
python -c "import anthropic; from google.auth import _helpers; import requests; print('✅ All packages installed')"
```

### 2. Test Configuration

```bash
# Verify environment variables are loaded
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('CLAUDE_API_KEY:', 'SET' if os.getenv('CLAUDE_API_KEY') else 'NOT SET')"
```

### 3. Test Processing (Single Cycle)

```bash
# Run one processing cycle
python -m src.claude_agent --mode once

# Watch logs
tail -f agent-one/logs/agent_one.log
```

### 4. Upload Test Video

1. Create a test video file (10-60 seconds)
2. Create a brief text file:
   ```
   test_video.mp4
   test_video_brief.txt
   
   # In test_video_brief.txt:
   This is a test meditation video.
   Cut pauses. Add calm ambient music.
   Warm color grade. Target Instagram.
   ```
3. Upload to Google Drive `/Agent-One-Inbox/`
4. Wait for agent to process (30 min max)
5. Check `/Agent-One-Outbox/` for results

---

## Monitoring & Logging

### Log Files

```
agent-one/
├── logs/
│   ├── agent_one.log              # Main agent log (real-time)
│   ├── processing_log_2026-08-16.txt  # Daily activity log
│   ├── completed_videos.json       # Record of processed videos
│   └── current_jobs.json           # Jobs in progress
├── temp/                           # Temporary processing files
└── cache/                          # Cache data
```

### View Logs

```bash
# Systemd service
sudo journalctl -u agent-one -f

# Docker container
docker logs -f agent-one

# Log files directly
tail -f agent-one/logs/agent_one.log

# JSON history
cat agent-one/logs/completed_videos.json | jq .
```

### Key Indicators

- ✅ `✅ Claude Agent One initialized` - Agent started successfully
- 📹 `Found X unprocessed video(s)` - Videos detected in inbox
- 🎬 `Starting processing for...` - Processing started
- ✅ `Video processing complete` - Video finished successfully
- ❌ `Error processing video` - Processing failed (check error message)

---

## Troubleshooting

### Issue: "No videos found in inbox"

**Causes:**
- Folder ID is wrong
- No videos in inbox
- Service account doesn't have access

**Fix:**
1. Verify folder ID: Open Drive → Share folder → Copy ID from URL
2. Check service account has access: In Drive, share folder with service account email
3. Verify folder path is exactly `/Agent-One-Inbox/`

### Issue: "FFmpeg not found"

**Causes:**
- FFmpeg not installed
- Wrong FFmpeg version

**Fix:**
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg

# Verify
ffmpeg -version
```

### Issue: "API key is invalid"

**Causes:**
- Wrong API key format
- API key not in .env
- API key expired/revoked

**Fix:**
1. Double-check API key in `.env`
2. Regenerate key from service
3. Make sure file is readable: `ls -la .env`

### Issue: "Service won't start"

**Check:**
```bash
# Systemd
sudo systemctl status agent-one
sudo journalctl -u agent-one -n 50

# Docker
docker logs agent-one | tail -50

# Check file permissions
ls -la /opt/agent-one
```

### Issue: "Slow processing"

**Causes:**
- Internet connection slow
- Server is underpowered
- Too many concurrent operations

**Fix:**
- Increase `PROCESSING_SCHEDULE_MINUTES` to reduce frequency
- Scale up server resources
- Check system load: `top` or `docker stats`

---

## Updating

### Update Code

```bash
cd agent-one
git pull origin main
pip install -r requirements.txt --upgrade
```

### Update Service

```bash
# For systemd
sudo systemctl restart agent-one

# For Docker
docker stop agent-one
docker build -t agent-one:latest .
docker run -d --name agent-one ... agent-one:latest
```

---

## Security Best Practices

1. **API Keys**: Store in `.env` file, never commit to git
2. **Service Account**: Use dedicated Google service account with minimal permissions
3. **Folder Sharing**: Only share with service account email, never public
4. **Logs**: Monitor for sensitive data leaks in logs
5. **Backups**: Regularly backup logs and completed_videos.json

---

## Performance Tuning

### Increase Processing Frequency

```bash
# Edit .env or service file
PROCESSING_SCHEDULE_MINUTES=15  # Check inbox every 15 minutes
```

### Optimize for Speed

```bash
# Edit config/constants.py
MAX_RETRIES=2  # Fewer retries
SILENCE_THRESHOLD_DB=-45  # Faster silence detection
```

### Optimize for Quality

```bash
# Edit config/constants.py
SILENCE_THRESHOLD_DB=-50  # Better quality
PLATFORM_SPECS['youtube']['crf'] = 20  # Higher quality (slower)
```

---

## Production Checklist

- [ ] All API keys configured and tested
- [ ] Google Drive folders created and shared
- [ ] FFmpeg installed and verified
- [ ] Single test video processed successfully
- [ ] Logs monitored and rotating properly
- [ ] Email notifications configured
- [ ] Systemd/Docker service auto-starts on reboot
- [ ] Backups configured for logs and state files
- [ ] Security audit: API keys, folder permissions, logs
- [ ] Documentation updated with actual folder IDs

---

## Support & Help

**Issues?** Check the logs first:
```bash
tail -f agent-one/logs/agent_one.log
```

**Need help?**
- Review processing log: `cat logs/processing_log_*.txt`
- Check job status: `cat logs/current_jobs.json | jq .`
- View API errors in logs

---

## Backup & Recovery

### Backup Important Data

```bash
# Backup completed videos record
cp agent-one/logs/completed_videos.json backups/completed_videos.json

# Backup logs
cp agent-one/logs/*.txt backups/

# Backup configuration
cp agent-one/.env backups/.env
```

### Recover from Failure

```bash
# Reset processing state (re-process all videos)
rm agent-one/logs/completed_videos.json
rm agent-one/logs/current_jobs.json

# Start service again
sudo systemctl restart agent-one
```

---

## Next Steps

1. **Deploy** using one of the methods above
2. **Configure** API keys and folder IDs
3. **Test** with a sample video
4. **Monitor** logs for successful processing
5. **Iterate** - try different briefs and content types
6. **Scale** - increase frequency or add more videos

**You're ready! Agent One is now live.** 🚀
