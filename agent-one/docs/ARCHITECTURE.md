# Agent One - System Architecture

## High-Level Overview

```
┌──────────────────────────────────────────────────────────────┐
│                       AGENT ONE SYSTEM                       │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ Input: Google Drive Inbox                             │ │
│  │ ├─ video.mp4                                          │ │
│  │ └─ video_brief.txt (voice instructions)              │ │
│  └────────────┬─────────────────────────────────────────┘ │
│               ▼                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ Agent Orchestrator (agent.py)                         │ │
│  │ ├─ Monitor schedule (every 30 min)                    │ │
│  │ ├─ Validate configuration                            │ │
│  │ └─ Coordinate processing pipeline                    │ │
│  └────────────┬─────────────────────────────────────────┘ │
│               ▼                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ Video Processor (video_processor.py)                  │ │
│  │ ├─ Step 1: Monitor & Detect                          │ │
│  │ ├─ Step 2: Download & Analyze                        │ │
│  │ ├─ Step 3: Parse Brief                              │ │
│  │ ├─ Step 4: Intelligent Edit                         │ │
│  │ ├─ Step 5: Transcribe                               │ │
│  │ ├─ Step 6: Generate Captions                        │ │
│  │ ├─ Step 7: Layer Music                              │ │
│  │ ├─ Step 8: Apply Finishing                          │ │
│  │ └─ Step 9: Upload & Create Summary                  │ │
│  └────────────┬─────────────────────────────────────────┘ │
│               ▼                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ Output: Google Drive Outbox                           │ │
│  │ ├─ video_instagram.mp4                               │ │
│  │ ├─ video_tiktok.mp4                                  │ │
│  │ ├─ video_youtube.mp4                                 │ │
│  │ ├─ video_linkedin.mp4                                │ │
│  │ └─ video_summary.txt                                 │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## Module Architecture

### Layer 1: Orchestration
```
┌─────────────────────────────────────────┐
│         Agent Orchestrator              │
│  (src/agent.py)                        │
├─────────────────────────────────────────┤
│ - Scheduled loop (30-min intervals)     │
│ - Configuration validation              │
│ - Job monitoring                        │
│ - Signal handling (graceful shutdown)   │
└────────────────────┬────────────────────┘
                     │
        ┌────────────┴────────────┐
        ▼                         ▼
    VideoProcessor      StateManager
    (coordinates)        (persists)
```

### Layer 2: Processing Pipeline
```
┌──────────────────────────────────────────────────┐
│  VideoProcessor (src/video_processor.py)        │
├──────────────────────────────────────────────────┤
│                                                  │
│  Step 1: Monitor    ▶ GoogleDriveClient         │
│  Step 2: Download   ▶ GoogleDriveClient         │
│  Step 3: Parse      ▶ ClaudeAPIClient           │
│  Step 4: Edit       ▶ FFmpegHandler             │
│  Step 5: Transcribe ▶ WhisperClient             │
│  Step 6: Captions   ▶ ClaudeAPIClient           │
│  Step 7: Music      ▶ PixabayMusicClient        │
│  Step 8: Finish     ▶ FFmpegHandler + Descript  │
│  Step 9: Upload     ▶ GoogleDriveClient         │
│                                                  │
└──────────────────────────────────────────────────┘
```

### Layer 3: External Services
```
┌─────────────────────────┐
│  Google Drive API       │
├─────────────────────────┤
│ - List files            │
│ - Download              │
│ - Upload                │
│ - Create folders        │
│ - Move files            │
└─────────────────────────┘

┌─────────────────────────┐       ┌──────────────────────┐
│  Claude API             │       │  OpenAI Whisper      │
├─────────────────────────┤       ├──────────────────────┤
│ - Parse briefs → JSON   │       │ - Transcribe audio   │
│ - Generate captions     │       │ - Extract timestamps │
│ - Decision making       │       └──────────────────────┘
└─────────────────────────┘

┌─────────────────────────┐       ┌──────────────────────┐
│  Pixabay Music API      │       │  Descript API        │
├─────────────────────────┤       ├──────────────────────┤
│ - Search music          │       │ - Color grading      │
│ - Download tracks       │       │ - Caption syncing    │
│ - License-free tracks   │       │ - Multi-format export│
└─────────────────────────┘       └──────────────────────┘

┌─────────────────────────┐
│  FFmpeg (System)        │
├─────────────────────────┤
│ - Video editing         │
│ - Audio processing      │
│ - Format conversion     │
│ - Resolution scaling    │
└─────────────────────────┘
```

### Layer 4: State & Configuration
```
┌──────────────────────────────────────┐
│  StateManager                        │
│  (src/state_manager.py)              │
├──────────────────────────────────────┤
│ - Job tracking                       │
│ - Completed videos log               │
│ - Current jobs tracking              │
│ - Daily activity log                 │
└──────────────────────────────────────┘

┌──────────────────────────────────────┐
│  Configuration                       │
│  (config/constants.py)               │
├──────────────────────────────────────┤
│ - API keys (from environment)        │
│ - Folder IDs (from environment)      │
│ - Platform specifications            │
│ - FFmpeg settings                    │
│ - Content type configurations        │
└──────────────────────────────────────┘
```

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    VIDEO PROCESSING FLOW                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. INPUT                                                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Google Drive /Agent-One-Inbox/                       │  │
│  │ ├─ video.mp4                                         │  │
│  │ └─ video_brief.txt                                  │  │
│  └──────────────┬───────────────────────────────────────┘  │
│                 │                                           │
│  2. DOWNLOAD    │ GoogleDriveClient.download_file()        │
│  ┌──────────────▼───────────────────────────────────────┐  │
│  │ /tmp/job_id/                                         │  │
│  │ ├─ video.mp4 (original)                             │  │
│  │ └─ brief.txt (instructions)                         │  │
│  └──────────────┬───────────────────────────────────────┘  │
│                 │                                           │
│  3. ANALYZE     │ FFmpegHandler.get_metadata()             │
│  ├─ Duration, resolution, audio specs                    │
│  │ FFmpegHandler.detect_silence()                        │
│  ├─ Silence segments for intelligent editing             │
│  │                                                       │
│  4. PARSE       │ ClaudeAPIClient.parse_brief()           │
│  └──────────────┬───────────────────────────────────────┘  │
│                 │                                           │
│  ┌──────────────▼───────────────────────────────────────┐  │
│  │ BRIEF JSON                                           │  │
│  │ {                                                    │  │
│  │   "content_type": "meditation",                      │  │
│  │   "duration_target": 300,                            │  │
│  │   "tone": ["dreamy", "peaceful"],                    │  │
│  │   "music": {"style": "ambient", ...},                │  │
│  │   "color_grade": {"warmth": 75, ...},                │  │
│  │   "platform_targets": ["instagram", ...]             │  │
│  │ }                                                    │  │
│  └──────────────┬───────────────────────────────────────┘  │
│                 │                                           │
│  5. EDIT        │ FFmpegHandler.remove_silence()           │
│                 │ FFmpegHandler.apply_color_grade()        │
│                 │ FFmpegHandler.normalize_audio()          │
│  ┌──────────────▼───────────────────────────────────────┐  │
│  │ /tmp/job_id/edited_video.mp4                         │  │
│  │ (silence removed, color adjusted)                    │  │
│  └──────────────┬───────────────────────────────────────┘  │
│                 │                                           │
│  6. TRANSCRIBE  │ FFmpegHandler.extract_audio()            │
│                 │ WhisperClient.transcribe()                │
│  ┌──────────────▼───────────────────────────────────────┐  │
│  │ TRANSCRIPT                                           │  │
│  │ "This is a peaceful meditation. Close your eyes..." │  │
│  │ (with timestamps for each phrase)                    │  │
│  └──────────────┬───────────────────────────────────────┘  │
│                 │                                           │
│  7. CAPTIONS    │ ClaudeAPIClient.generate_captions()      │
│  ┌──────────────▼───────────────────────────────────────┐  │
│  │ PLATFORM CAPTIONS                                    │  │
│  │ ├─ Instagram: "Find peace in 5 minutes... 🧘"        │  │
│  │ ├─ TikTok: "Calm your mind now..."                   │  │
│  │ ├─ YouTube: "Learn this ancient breathing..."        │  │
│  │ └─ LinkedIn: "Professional meditation guide..."      │  │
│  └──────────────┬───────────────────────────────────────┘  │
│                 │                                           │
│  8. MUSIC       │ PixabayMusicClient.search_music()        │
│                 │ PixabayMusicClient.download_music()      │
│                 │ FFmpegHandler.layer_audio()              │
│  ┌──────────────▼───────────────────────────────────────┐  │
│  │ /tmp/job_id/video_with_music.mp4                     │  │
│  │ (voice -3dB + music -12dB = balanced mix)            │  │
│  └──────────────┬───────────────────────────────────────┘  │
│                 │                                           │
│  9. EXPORT      │ FFmpegHandler.resize_and_export()        │
│  ┌──────────────▼───────────────────────────────────────┐  │
│  │ /tmp/job_id/                                         │  │
│  │ ├─ output_instagram.mp4 (1080×1350)                 │  │
│  │ ├─ output_tiktok.mp4 (1080×1920)                    │  │
│  │ ├─ output_youtube.mp4 (1080×1920)                   │  │
│  │ └─ output_linkedin.mp4 (1200×628)                   │  │
│  └──────────────┬───────────────────────────────────────┘  │
│                 │                                           │
│  10. UPLOAD     │ GoogleDriveClient.create_folder()        │
│                 │ GoogleDriveClient.upload_file() × 4      │
│  ┌──────────────▼───────────────────────────────────────┐  │
│  │ OUTPUT                                               │  │
│  │ Google Drive /Agent-One-Outbox/video_name/           │  │
│  │ ├─ video_instagram.mp4 ✅                            │  │
│  │ ├─ video_tiktok.mp4 ✅                               │  │
│  │ ├─ video_youtube.mp4 ✅                              │  │
│  │ ├─ video_linkedin.mp4 ✅                             │  │
│  │ └─ video_summary.txt ✅                              │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  11. STATE      │ StateManager.complete_job()              │
│  └─ Mark in completed_videos.json                        │
│  └─ Log to processing_log_{date}.txt                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Class Hierarchy

```
StateManager
├─ ProcessingJob (dataclass)
│  ├─ video_id: str
│  ├─ status: str (pending, processing, completed, failed)
│  ├─ content_type: str
│  ├─ platforms: List[str]
│  └─ output_paths: Dict[str, str]
│
├─ load_completed_videos()
├─ load_current_jobs()
├─ create_job()
├─ update_job()
├─ complete_job()
└─ fail_job()

VideoProcessor
├─ __init__()
│  ├─ state: StateManager
│  ├─ drive: GoogleDriveClient
│  ├─ ffmpeg: FFmpegHandler
│  ├─ claude: ClaudeAPIClient
│  ├─ whisper: WhisperClient
│  ├─ descript: DescriptClient
│  └─ pixabay: PixabayMusicClient
│
├─ process_video() → main entry point
├─ _process_single_video() → per-video pipeline
├─ _edit_video() → content-aware editing
├─ _add_music() → music layering
├─ _export_platforms() → multi-format export
├─ _upload_to_outbox() → finalization
└─ _create_summary() → summary file

GoogleDriveClient
├─ authenticate()
├─ list_files_in_folder()
├─ find_video_and_brief()
├─ download_file()
├─ upload_file()
├─ create_folder()
├─ move_file()
└─ delete_file()

FFmpegHandler
├─ get_video_metadata()
├─ detect_silence()
├─ remove_silence()
├─ normalize_audio()
├─ apply_color_grade()
├─ extract_audio()
├─ layer_audio()
└─ resize_and_export()

ClaudeAPIClient
├─ parse_brief() → voice text → JSON
├─ generate_captions() → transcript → 4 captions
├─ estimate_captions_from_video() → fallback
├─ validate_brief_json()
└─ get_caption_confidence_score()

WhisperClient
└─ transcribe() → audio file → transcript + timestamps

PixabayMusicClient
├─ search_music()
└─ download_music()

DescriptClient
└─ process_video() → color grading, export (simplified)

AgentOne
├─ validate_config()
├─ run_once()
├─ run_scheduled()
└─ run_once_mode()
```

## Error Handling Flow

```
Processing Error
    │
    ├─► FFmpeg fails
    │   ├─ Log error
    │   ├─ Move to /Errors
    │   ├─ Set job status = "failed"
    │   └─ Retry after 1 hour (3 max)
    │
    ├─► Whisper fails
    │   ├─ Retry (Whisper is reliable)
    │   ├─ If 3 failures: fallback to Claude
    │   └─ Continue processing
    │
    ├─► Descript fails
    │   ├─ Retry with exponential backoff
    │   ├─ If fails: fallback to FFmpeg basic export
    │   └─ Continue (lower quality but functional)
    │
    ├─► Music unavailable
    │   ├─ Skip music layer
    │   ├─ Process without music
    │   ├─ Notify user in summary
    │   └─ Continue processing
    │
    └─► Google Drive fails
        ├─ Log error with timestamp
        ├─ Retry up to 3 times
        ├─ Set job status = "failed"
        └─ Move video to /Errors
```

## Scheduling & Automation

```
┌─────────────────────────────────────────┐
│       Scheduled Execution               │
│  (30-minute intervals, configurable)    │
├─────────────────────────────────────────┤
│                                         │
│ Minute 0:                               │
│ ├─ Agent wakes up                      │
│ ├─ Validates config                    │
│ └─ Starts processing cycle              │
│                                         │
│ Minute 0-50:                            │
│ ├─ Process videos in sequence          │
│ ├─ Each takes 35-50 min                │
│ └─ Update state continuously            │
│                                         │
│ Minute 50-60:                           │
│ ├─ Finish processing                   │
│ ├─ Upload to outbox                    │
│ ├─ Log activity                         │
│ └─ Wait for next cycle                  │
│                                         │
│ Minute 30:                              │
│ ├─ Check for new videos                │
│ ├─ Start processing next batch         │
│ └─ Loop continues...                    │
│                                         │
└─────────────────────────────────────────┘
```

## Configuration Hierarchy

```
Level 1: Defaults (constants.py)
├─ Processing schedule: 30 minutes
├─ Silence threshold: -50dB
├─ Audio normalization: -3dB
├─ Music volume: -12dB
├─ Max retries: 3
└─ Content type settings

Level 2: Environment Variables (.env)
├─ API keys (Claude, Whisper, etc.)
├─ Folder IDs (Inbox, Outbox, Logs, Errors)
└─ Optional overrides

Level 3: Runtime (command-line args)
├─ Mode (scheduled vs once)
└─ Interval override (for scheduled mode)
```

## Performance Characteristics

```
Single Video Processing:
├─ Step 1 (Download & Analyze): 2 min
├─ Step 2 (Parse Brief): 1 min
├─ Step 3 (Edit): 10-15 min (depends on silence)
├─ Step 4 (Transcribe): 3 min (depends on audio length)
├─ Step 5 (Captions): 3 min
├─ Step 6 (Music): 5 min
├─ Step 7 (Finishing): 5 min
├─ Step 8 (Export × 4): 10-15 min
└─ Step 9 (Upload): 2 min
   TOTAL: 35-50 minutes

System Resources:
├─ CPU: 50-100% (video encoding is CPU-intensive)
├─ Memory: 500MB - 2GB (depends on video size)
├─ Disk: 3-5× video file size (for temp/processing)
├─ Network: 1-2 Mbps (Google Drive uploads)
└─ Scalability: Linear (one video at a time)
```

## Deployment Architectures

### Development
```
┌─────────────────────┐
│  Developer Machine  │
├─────────────────────┤
│ Python venv         │
│ Agent One running   │
│ (--mode once)       │
└─────────────────────┘
```

### Production (Cron)
```
┌─────────────────────────────┐
│    Linux Server             │
├─────────────────────────────┤
│ Cron Job (every 30 min)     │
│ └─ python agent.py --mode once
│                             │
│ Logs → Google Drive         │
│ State → Google Drive        │
│ Videos → Google Drive       │
└─────────────────────────────┘
```

### Production (Systemd)
```
┌──────────────────────────────┐
│    Linux Server              │
├──────────────────────────────┤
│ systemd Service              │
│ └─ python agent.py --mode    │
│    scheduled                 │
│                              │
│ Auto-restart on failure      │
│ Logs → journalctl            │
│ State → Google Drive         │
└──────────────────────────────┘
```

### Production (Docker)
```
┌────────────────────────────────┐
│  Docker Container              │
├────────────────────────────────┤
│ ├─ Python 3.11                │
│ ├─ FFmpeg installed            │
│ ├─ Agent One code              │
│ └─ python agent.py scheduled   │
│                                │
│ Deployed on:                   │
│ ├─ Kubernetes                  │
│ ├─ Docker Swarm                │
│ └─ Cloud services              │
└────────────────────────────────┘
```

---

This architecture provides:
- ✅ Clear separation of concerns
- ✅ Easy testing and debugging
- ✅ Scalability for future enhancements
- ✅ Robust error handling
- ✅ Complete auditability
- ✅ Production-ready design
