# Agent One - Troubleshooting Guide

## Common Issues and Solutions

### Setup Issues

#### FFmpeg not found

**Error:**
```
FFmpeg not found: [Errno 2] No such file or directory: 'ffmpeg'
```

**Solutions:**

Linux (Ubuntu/Debian):
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

macOS:
```bash
brew install ffmpeg
```

Windows:
```bash
choco install ffmpeg
# Or download from https://ffmpeg.org/download.html
```

Verify:
```bash
ffmpeg -version
ffprobe -version
```

---

#### Python dependencies missing

**Error:**
```
ModuleNotFoundError: No module named 'anthropic'
```

**Solution:**
```bash
pip install -r requirements.txt --upgrade
```

If specific module fails:
```bash
pip install anthropic google-auth openai requests --upgrade
```

---

### Authentication Issues

#### Google Drive authentication failed

**Error:**
```
Failed to authenticate with Google Drive: ...
```

**Causes & Solutions:**

1. **Invalid JSON format:**
   - Check GOOGLE_DRIVE_OAUTH_JSON is valid JSON
   - Copy entire content of service account JSON file
   - No trailing commas or missing brackets

2. **Service account doesn't have access:**
   - Share folders with service account email: `agent-one@project-id.iam.gserviceaccount.com`
   - Give "Editor" permissions
   - Wait 1 minute for propagation

3. **Wrong project:**
   - Verify Google Drive API is enabled in same project
   - Check service account is in correct project

**Debug:**
```bash
python -c "
import json
import os
try:
    sa_json = os.getenv('GOOGLE_DRIVE_OAUTH_JSON')
    json.loads(sa_json)
    print('✅ JSON is valid')
except Exception as e:
    print(f'❌ JSON error: {e}')
"
```

---

#### API key errors

**Error:**
```
Invalid API key: sk-...
```

**Solutions:**

1. **Wrong API key:**
   - Double-check you copied the entire key
   - Verify it's the correct service (Claude, Whisper, etc.)
   - Check for leading/trailing spaces

2. **Key expired or revoked:**
   - Log in to service console
   - Generate a new API key
   - Update .env file

3. **Wrong environment variable name:**
   - Check: CLAUDE_API_KEY (not CLAUDE_KEY)
   - Check: WHISPER_API_KEY (not OPENAI_API_KEY)
   - Check: DESCRIPT_API_KEY (not DESCRIPT_KEY)

**Debug:**
```bash
echo $CLAUDE_API_KEY  # Should show your key
```

---

### Video Processing Issues

#### "No videos found to process"

**Possible causes:**

1. **Wrong folder structure:**
   - ❌ Video in wrong folder
   - ✅ Both video and brief in `/Agent-One-Inbox/`
   - ❌ Brief file in different folder

2. **Wrong brief file name:**
   - ❌ `test_instructions.txt`
   - ✅ `test_brief.txt`
   - Format: `{VIDEO_NAME}_brief.txt`

3. **Folder ID is wrong:**
   - Get ID from URL: `https://drive.google.com/drive/folders/{ID}`
   - Check AGENT_ONE_INBOX_FOLDER_ID environment variable
   - Verify service account has access

**Fix:**
```bash
# Check logs
tail -f logs/agent_one.log

# Verify folder IDs
echo $AGENT_ONE_INBOX_FOLDER_ID
echo $AGENT_ONE_OUTBOX_FOLDER_ID

# Test manually
python -c "
from src.google_drive_client import GoogleDriveClient
client = GoogleDriveClient()
files = client.list_files_in_folder('YOUR_FOLDER_ID')
print(f'Found {len(files)} files')
"
```

---

#### "FFmpeg processing failed"

**Error:**
```
Error in remove_silence: ffmpeg command failed
```

**Common causes:**

1. **Corrupted video file:**
   - Try with a different video
   - Verify video plays normally
   - Check file size is reasonable

2. **Unsupported codec:**
   - Agent One supports: MP4, MOV, AVI, MKV
   - Convert to MP4: `ffmpeg -i input.mov -c copy output.mp4`

3. **Insufficient disk space:**
   - Check: `df -h`
   - Clean up `/agent-one/temp/` directory
   - Ensure at least 5GB free space

4. **FFmpeg version issue:**
   - Update FFmpeg: `brew upgrade ffmpeg` (macOS)
   - Or reinstall: `apt-get install --only-upgrade ffmpeg` (Linux)

**Debug:**
```bash
# Test FFmpeg with your video
ffmpeg -i your_video.mp4 -af "silencedetect=n=-50dB:d=0.5" -f null -

# Check video format
ffprobe your_video.mp4
```

---

#### "Whisper transcription failed"

**Error:**
```
Error transcribing with Whisper: ...
```

**Causes & Solutions:**

1. **Invalid API key:**
   - Check WHISPER_API_KEY is set
   - Verify key is from OpenAI (not Claude)
   - Check key hasn't expired

2. **Audio too long:**
   - Whisper has practical limits (~25MB files)
   - Agent One will retry automatically

3. **No audio in video:**
   - Video must have audio track
   - Audio must be audible (not silent)

4. **Network error:**
   - Check internet connection
   - Agent will retry after 1 hour

**Fallback:**
- If Whisper fails 3 times, Agent uses Claude to estimate captions from video
- Quality will be lower, but processing continues

---

#### "Brief parsing failed"

**Error:**
```
Failed to parse Claude response as JSON
```

**Causes:**

1. **Claude API key invalid:**
   - Check CLAUDE_API_KEY is set
   - Verify key is from Anthropic
   - Try generating new key

2. **Brief text is empty:**
   - Brief file must have content
   - Check brief file encoding (UTF-8)

3. **Brief is too vague:**
   - Agent couldn't parse instructions
   - Try being more specific: "meditation", "remove pauses", "warm tone"

**How to write better briefs:**

❌ Bad: "edit the video"
✅ Good: "This is meditation. Remove long pauses. Add ambient music. Warm color grade."

Include:
- Content type (meditation, vlog, speech)
- Specific edits needed (remove pauses, remove ums)
- Music style (ambient, upbeat, etc.)
- Color tone (warm, cool, vibrant)
- Target platform (Instagram, TikTok, YouTube, LinkedIn)

---

#### "Output files not created"

**Problem:** Video processed but no output files in outbox

**Causes:**

1. **Folder ID is wrong:**
   - Check AGENT_ONE_OUTBOX_FOLDER_ID
   - Verify service account has "Editor" access
   - Try re-sharing folder

2. **Descript API not working:**
   - Descript integration is simplified
   - Check DESCRIPT_API_KEY is set
   - Some features may require manual setup

3. **Permission denied:**
   - Service account doesn't have write access
   - Share outbox folder again with agent email
   - Give "Editor" permissions

**Check:**
```bash
# Look for temp files
ls -la temp/

# Check logs for errors
grep -i "error" logs/agent_one.log
```

---

### Performance Issues

#### Processing very slow

**Normal timings:**
- Per video: 35-50 minutes
- Depends on: video length, API response time, file size

**If slower than normal:**

1. **Large video file:**
   - Process shorter videos first
   - Reduce resolution before uploading

2. **API delays:**
   - Whisper API can be slow (depends on audio length)
   - Claude API responds in seconds usually
   - Check internet speed: `speedtest-cli`

3. **Disk I/O bottleneck:**
   - Check disk speed: `dd if=/dev/zero of=test.img bs=1M count=100 && rm test.img`
   - Ensure enough disk space
   - Consider SSD vs. HDD

**Optimize:**
```bash
# Check system resources
htop  # CPU/RAM usage
df -h  # Disk space
iostat  # I/O stats
```

---

#### Agent crashes or stops

**Causes:**

1. **Out of disk space:**
   ```bash
   df -h  # Check available space
   rm -rf temp/*  # Clean temp files
   ```

2. **Out of memory:**
   - Agent tries to process very large videos
   - Limit video size: < 500MB
   - Check RAM: `free -h`

3. **Network timeout:**
   - Agent will retry automatically
   - Check internet: `ping google.com`
   - Restart agent: `Ctrl+C` then restart

4. **Stale process:**
   ```bash
   # Find agent process
   ps aux | grep "python.*agent"
   
   # Kill it
   kill -9 PID
   
   # Restart
   python src/agent.py --mode scheduled
   ```

---

### Logging Issues

#### Can't find logs

**Logs should be in:**
```
agent-one/logs/
├── agent_one.log              # Main log
├── processing_log_2026-08-16.txt  # Daily log
├── completed_videos.json       # Processed videos
└── current_jobs.json           # In-progress jobs
```

**If missing:**
```bash
# Create logs directory
mkdir -p logs

# Check permissions
ls -la logs/

# Start agent again
python src/agent.py --mode once
```

---

#### Logs are too verbose

**Control log level in constants.py:**
```python
# Change from DEBUG to INFO or WARNING
logging.basicConfig(level=logging.INFO)
```

Or filter logs:
```bash
# View only errors
grep ERROR logs/agent_one.log

# View only INFO messages
grep INFO logs/agent_one.log

# Last 20 lines
tail -20 logs/agent_one.log
```

---

### Google Drive Issues

#### "Folder not found"

**Error:**
```
Error listing files: ...
```

**Solutions:**

1. **Folder ID is wrong:**
   - Open folder in Google Drive
   - Copy exact ID from URL bar
   - No extra characters or spaces

2. **Service account doesn't have access:**
   - Share folder with: `agent-one@project-id.iam.gserviceaccount.com`
   - Give "Editor" permissions
   - Click "Share" not just "Get link"

3. **Folder was deleted:**
   - Recreate the folder
   - Share again with service account
   - Update environment variable

**Test access:**
```bash
python -c "
from src.google_drive_client import GoogleDriveClient
client = GoogleDriveClient()
files = client.list_files_in_folder('YOUR_FOLDER_ID')
print(f'✅ Found {len(files)} files')
"
```

---

#### Files not uploading to outbox

**Causes:**

1. **No write permission:**
   - Verify service account has "Editor" access
   - Re-share outbox folder
   - Wait 1-2 minutes for permission propagation

2. **Quota exceeded:**
   - Google Drive quota full
   - Delete old files to free space
   - Check: [Google One storage](https://one.google.com)

3. **Filename conflict:**
   - Agent renames file if duplicate exists
   - Check outbox for similar filenames

**Check:**
```bash
# View agent's recent activity
tail -50 logs/agent_one.log | grep -i "upload\|outbox"
```

---

## Getting Help

### What to include when asking for help:

1. **Error message** (from logs)
2. **Steps you took** to trigger the error
3. **Configuration** (API keys set? Folders shared?)
4. **Log file** (last 50 lines of agent_one.log)
5. **System info** (Python version, OS, FFmpeg version)

### Debug checklist:

- [ ] Check all environment variables are set: `env | grep AGENT_ONE`
- [ ] Verify FFmpeg is installed: `ffmpeg -version`
- [ ] Test Google Drive access: `python -c "from google_drive_client import *"`
- [ ] Check logs: `tail -100 logs/agent_one.log`
- [ ] Verify API keys: `echo $CLAUDE_API_KEY | head -c 20`...
- [ ] Check disk space: `df -h`
- [ ] Check internet: `ping google.com`

### Still stuck?

1. Check logs carefully for exact error
2. Review this guide for similar issues
3. Test components individually
4. Review SETUP.md again
5. Contact support with logs

---

## Recovery Procedures

### Reset agent state

```bash
# Delete state files (clears processing history)
rm logs/completed_videos.json
rm logs/current_jobs.json

# Agent will re-process any videos in inbox
```

### Clean temporary files

```bash
# Remove all temporary processing files
rm -rf temp/*

# Remove cache
rm -rf cache/*

# Note: This is safe, next videos will recreate cache
```

### Restart fresh

```bash
# Stop agent
Ctrl+C

# Delete all state
rm -rf logs/* temp/* cache/*

# Create new directories
mkdir -p logs temp cache

# Restart
python src/agent.py --mode once
```

### Manual cleanup

```bash
# Find processes
ps aux | grep agent

# Kill process
kill -9 PID

# Remove lock files
rm -f .agent.lock

# Check disk usage
du -sh .

# Free up space
rm -rf temp/*
```

---

## Performance Tuning

### For faster processing:

1. **Increase system resources:**
   - More CPU cores help parallel processing
   - More RAM helps with large video files
   - SSD faster than HDD

2. **Optimize video files:**
   - Smaller videos process faster
   - Lower resolution = faster export
   - Pre-transcode to H.264

3. **Adjust FFmpeg settings in constants.py:**
   ```python
   # Faster but lower quality
   AUDIO_NORMALIZATION_DB = -6  # Instead of -3
   
   # Skip some processing
   # (not recommended for production)
   ```

---

**For more help, see:**
- [SETUP.md](./SETUP.md) - Detailed setup guide
- [QUICK_START.md](./QUICK_START.md) - Quick start
- Main [README.md](../README.md) - Overview
