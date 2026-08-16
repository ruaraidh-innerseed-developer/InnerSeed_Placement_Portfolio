# Agent One - Quick Start (10 minutes)

Get Agent One running in under 10 minutes.

---

## 5-Minute Setup

### Step 1: Prerequisites (2 min)

```bash
# Install FFmpeg (critical for video processing)
sudo apt-get update && sudo apt-get install ffmpeg python3-pip

# Verify
ffmpeg -version
python3 --version
```

### Step 2: Clone & Configure (3 min)

```bash
# Clone repository
cd /opt  # or your preferred location
git clone https://github.com/ruaraidh-innerseed-developer/InnerSeed_Placement_Portfolio.git
cd InnerSeed_Placement_Portfolio/agent-one

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
nano .env  # Edit with your API keys
```

### Step 3: Get API Keys (5 min - do this in parallel)

While editing `.env`, gather these API keys:

1. **Claude API** (2 min)
   - Go to: https://console.anthropic.com
   - Create API key
   - Paste in `.env`: `CLAUDE_API_KEY=sk-ant-...`

2. **Google Drive Service Account** (2 min)
   - Go to: https://console.cloud.google.com
   - Create Service Account
   - Download JSON file
   - Paste contents in `.env`: `GOOGLE_DRIVE_OAUTH_JSON={...}`

3. **Whisper API** (1 min)
   - Go to: https://platform.openai.com/api-keys
   - Create API key
   - Paste in `.env`: `WHISPER_API_KEY=sk-...`

4. **Descript API** (copy from account settings)
   - Paste in `.env`: `DESCRIPT_API_KEY=...`

5. **Pixabay Music API** (copy from account)
   - Paste in `.env`: `PIXABAY_API_KEY=...`

### Step 4: Get Google Drive Folder IDs (3 min)

In Google Drive:

1. Create folders:
   - `/Agent-One-Inbox/`
   - `/Agent-One-Outbox/`
   - `/Agent-One-Logs/`
   - `/Agent-One-Errors/`

2. For each folder:
   - Right-click → Share
   - Copy link
   - Extract ID: `https://drive.google.com/drive/folders/FOLDER_ID_HERE`
   - Paste into `.env`:
     ```
     AGENT_ONE_INBOX_FOLDER_ID=...
     AGENT_ONE_OUTBOX_FOLDER_ID=...
     AGENT_ONE_LOGS_FOLDER_ID=...
     AGENT_ONE_ERRORS_FOLDER_ID=...
     ```

3. Share all folders with service account email:
   - Your service account email: (from the JSON file: "client_email")
   - Add this email to folder sharing

---

## Deploy (Choose One)

### Option A: Systemd Service (Recommended)

```bash
# Automated setup
chmod +x deploy.sh
sudo ./deploy.sh
# Choose option 1 for systemd

# Start the service
sudo systemctl start agent-one
sudo systemctl enable agent-one  # Auto-start on reboot

# Check status
sudo systemctl status agent-one

# Watch logs
sudo journalctl -u agent-one -f
```

### Option B: Docker

```bash
chmod +x deploy.sh
./deploy.sh
# Choose option 2

# Start container
docker run -d \
  --name agent-one \
  --env-file .env \
  -v $(pwd)/logs:/app/logs \
  agent-one:latest

# Watch logs
docker logs -f agent-one
```

### Option C: Simple Cron (Minimal Setup)

```bash
crontab -e

# Add this line (runs every 30 minutes):
*/30 * * * * cd /path/to/agent-one && python -m src.claude_agent --mode once >> logs/cron.log 2>&1
```

### Option D: Manual Test First

```bash
# Run one processing cycle
python -m src.claude_agent --mode once

# Watch the log
tail -f logs/agent_one.log
```

---

## Test It (5 minutes)

### 1. Create Test Video (1 min)

Use your phone or any video app to create a short video:
- Title: `meditation_test.mp4`
- Duration: 10-60 seconds
- Content: Whatever you want

### 2. Create Brief File (1 min)

Create text file `meditation_test_brief.txt`:

```
This is a test meditation video.
Remove any long pauses.
Add calm ambient background music.
Apply a warm, spiritual color grade.
Target Instagram Reels (max 90 seconds).
```

### 3. Upload to Inbox (1 min)

Upload both files to Google Drive:
```
/Agent-One-Inbox/
├─ meditation_test.mp4
└─ meditation_test_brief.txt
```

### 4. Wait & Check (2 min)

- If **systemd/docker/cron**: Agent runs automatically, check inbox
  - Check logs: `tail -f logs/agent_one.log`
  - Or manually run: `python -m src.claude_agent --mode once`

- If **manual mode**: Run now:
  ```bash
  python -m src.claude_agent --mode once
  ```

### 5. Find Results

Check Google Drive `/Agent-One-Outbox/`:
```
/meditation_test/
├─ meditation_test_instagram.mp4
├─ meditation_test_tiktok.mp4
├─ meditation_test_youtube.mp4
├─ meditation_test_linkedin.mp4
└─ meditation_test_summary.txt
```

✅ **Success!** Agent One is working!

---

## What to Expect

### Processing Time: 35-50 minutes

```
0 min:   Upload video + brief to inbox
5 min:   Agent downloads and analyzes
6 min:   Claude parses your instructions
20 min:  Video editing + color grading
25 min:  Transcription complete
30 min:  Captions generated
35 min:  Music layered
50 min:  ✅ DONE - Check outbox!
```

### Sample Output

Each video produces:

1. **4 Video Files** (platform-optimized):
   - `meditation_test_instagram.mp4` (1080x1350)
   - `meditation_test_tiktok.mp4` (1080x1920)
   - `meditation_test_youtube.mp4` (1080x1920)
   - `meditation_test_linkedin.mp4` (1200x628 + 1920x1080)

2. **Summary File** with:
   - Processing details
   - 4 platform-specific captions
   - Technical specs
   - Status ready for posting

---

## Troubleshooting (5 minutes)

### "No videos found"

```bash
# Check folder ID is correct
echo $AGENT_ONE_INBOX_FOLDER_ID

# Verify service account has access
# Go to Google Drive → Inbox folder → Share
# Confirm service account email is added
```

### "FFmpeg not found"

```bash
# Install FFmpeg
sudo apt-get install ffmpeg

# Verify
ffmpeg -version
```

### "API key invalid"

```bash
# Check .env file
cat .env | grep API_KEY

# Verify format
# CLAUDE_API_KEY should start with: sk-ant-
# WHISPER_API_KEY should start with: sk-
# DESCRIPT_API_KEY should be: 20+ character string
# PIXABAY_API_KEY should be: alphanumeric string
```

### "Agent won't start"

```bash
# Check logs
tail -f logs/agent_one.log

# Test environment
python -c "import anthropic; from google.auth import _helpers; print('✅ Packages OK')"

# Try manual run
python -m src.claude_agent --mode once
```

### "Processing seems stuck"

```bash
# Check what's processing
cat logs/current_jobs.json | jq .

# Check if still running
ps aux | grep claude_agent

# Monitor system
top  # Check CPU/memory usage
df   # Check disk space
```

---

## Next Steps

### 1. Upload More Videos

Upload as many videos as you want to `/Agent-One-Inbox/`:
```
video1.mp4 + video1_brief.txt
video2.mp4 + video2_brief.txt
video3.mp4 + video3_brief.txt
...
```

Agent processes one every 30-50 minutes.

### 2. Write Better Briefs

The more detailed your brief, the better the results:

```
Bad brief:
"Edit this video"

Good brief:
"Energetic vlog about my morning routine.
Remove long pauses and filler words (ums, ahs).
Add upbeat pop music underneath.
Bright, vibrant color grade.
Keep it 3-5 minutes.
Export for TikTok and Instagram."
```

### 3. Monitor Regularly

```bash
# Watch logs while processing
tail -f logs/agent_one.log

# Check completed videos
cat logs/completed_videos.json | jq .

# Monitor system
docker stats  # If using Docker
```

### 4. Scale Up

Once working, you can:
- Decrease schedule interval (process more frequently)
- Add more API quota
- Deploy to more powerful server
- Process multiple videos in parallel (advanced)

---

## Common Questions

**Q: Can I edit the agent while it's processing?**
A: Yes! The agent is stateless. Stop it, edit, restart.

**Q: Can I process multiple videos at once?**
A: Currently processes one per cycle. Multiple cycles = parallel processing.

**Q: What if processing fails?**
A: Video moves to `/Agent-One-Errors/`. Check logs for error. Fix and re-upload.

**Q: Can I change processing settings?**
A: Edit `config/constants.py` to adjust silence detection, music volume, etc.

**Q: How do I update the code?**
A: `git pull` → update `.env` if needed → restart service.

**Q: Is my data safe?**
A: All processing happens locally. Only outputs go to Google Drive.

---

## Production Checklist

Before going live:

- [ ] All API keys configured and working
- [ ] Google Drive folders created and shared
- [ ] Test video processed successfully
- [ ] Logs configured to rotate
- [ ] Service set to auto-start on reboot
- [ ] Email notifications configured (optional)
- [ ] Backup strategy in place
- [ ] Monitoring logs set up

---

## Get Help

**Still stuck?** Check in this order:

1. **Logs**: `tail -f logs/agent_one.log`
2. **Status**: `cat logs/current_jobs.json | jq .`
3. **Docs**: Read `docs/DEPLOYMENT.md`
4. **Config**: Verify `.env` file has all keys

---

**🎉 You're done! Agent One is now processing videos autonomously.** 

Go upload a video to `/Agent-One-Inbox/` and watch the magic happen! ✨
