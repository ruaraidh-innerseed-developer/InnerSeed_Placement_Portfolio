"""
Agent One Dashboard - Web UI for monitoring and managing the agent
Real-time status, job history, logs, and controls
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import json
import os
from pathlib import Path
from datetime import datetime, timedelta
import threading
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Paths
LOG_DIR = Path(__file__).parent.parent / "logs"
COMPLETED_VIDEOS_FILE = LOG_DIR / "completed_videos.json"
CURRENT_JOBS_FILE = LOG_DIR / "current_jobs.json"
AGENT_LOG_FILE = LOG_DIR / "agent_one.log"


class DashboardData:
    """Manages dashboard data"""

    @staticmethod
    def get_current_jobs():
        """Get currently processing jobs"""
        if not CURRENT_JOBS_FILE.exists():
            return []
        try:
            with open(CURRENT_JOBS_FILE) as f:
                jobs = json.load(f)
                return list(jobs.values())
        except:
            return []

    @staticmethod
    def get_completed_videos(days=7):
        """Get completed videos from last N days"""
        if not COMPLETED_VIDEOS_FILE.exists():
            return []
        try:
            with open(COMPLETED_VIDEOS_FILE) as f:
                videos = json.load(f)
                cutoff = datetime.now() - timedelta(days=days)
                return [
                    {
                        "name": name,
                        "completed_at": data.get("completed_at"),
                        "platforms": data.get("platforms", []),
                    }
                    for name, data in videos.items()
                    if datetime.fromisoformat(data.get("completed_at", "")) > cutoff
                ]
        except:
            return []

    @staticmethod
    def get_stats():
        """Get dashboard statistics"""
        current_jobs = DashboardData.get_current_jobs()
        completed = DashboardData.get_completed_videos(days=1)

        return {
            "current_processing": len(current_jobs),
            "completed_today": len(completed),
            "total_completed": len(
                json.load(open(COMPLETED_VIDEOS_FILE))
                if COMPLETED_VIDEOS_FILE.exists()
                else {}
            ),
            "uptime": get_uptime(),
            "next_check": get_next_check_time(),
            "storage_used": get_storage_usage(),
        }

    @staticmethod
    def get_recent_logs(lines=100):
        """Get recent log lines"""
        if not AGENT_LOG_FILE.exists():
            return []
        try:
            with open(AGENT_LOG_FILE) as f:
                log_lines = f.readlines()
                return log_lines[-lines:]
        except:
            return []


def get_uptime():
    """Get agent uptime"""
    # Check systemd service uptime
    try:
        import subprocess

        result = subprocess.run(
            ["systemctl", "show", "agent-one", "-p", "ActiveEnterTimestamp"],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except:
        pass
    return "Unknown"


def get_next_check_time():
    """Get next scheduled check time"""
    now = datetime.now()
    minutes_to_next = 30 - (now.minute % 30)
    next_check = now + timedelta(minutes=minutes_to_next)
    return next_check.strftime("%H:%M:%S")


def get_storage_usage():
    """Get storage usage"""
    temp_dir = Path(__file__).parent.parent / "temp"
    if not temp_dir.exists():
        return 0
    total = sum(f.stat().st_size for f in temp_dir.rglob("*") if f.is_file())
    return f"{total / (1024**2):.1f}MB"


# API Routes

@app.route("/api/status")
def api_status():
    """Get agent status"""
    return jsonify(
        {
            "status": "running",
            "stats": DashboardData.get_stats(),
            "timestamp": datetime.now().isoformat(),
        }
    )


@app.route("/api/current-jobs")
def api_current_jobs():
    """Get current processing jobs"""
    return jsonify({"jobs": DashboardData.get_current_jobs()})


@app.route("/api/completed-videos")
def api_completed_videos():
    """Get completed videos"""
    days = request.args.get("days", 7, type=int)
    return jsonify({"videos": DashboardData.get_completed_videos(days=days)})


@app.route("/api/stats")
def api_stats():
    """Get dashboard statistics"""
    return jsonify(DashboardData.get_stats())


@app.route("/api/logs")
def api_logs():
    """Get recent logs"""
    lines = request.args.get("lines", 100, type=int)
    return jsonify({"logs": DashboardData.get_recent_logs(lines=lines)})


@app.route("/api/restart")
def api_restart():
    """Restart agent service"""
    try:
        import subprocess

        subprocess.run(["sudo", "systemctl", "restart", "agent-one"], check=True)
        return jsonify({"status": "success", "message": "Agent restarted"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/api/logs-clear")
def api_logs_clear():
    """Clear logs"""
    try:
        if AGENT_LOG_FILE.exists():
            AGENT_LOG_FILE.write_text("")
        return jsonify({"status": "success", "message": "Logs cleared"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# Pages

@app.route("/")
def dashboard():
    """Main dashboard page"""
    return render_template("index.html")


@app.route("/jobs")
def jobs_page():
    """Jobs history page"""
    return render_template("jobs.html")


@app.route("/logs")
def logs_page():
    """Logs viewer page"""
    return render_template("logs.html")


@app.route("/settings")
def settings_page():
    """Settings page"""
    return render_template("settings.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
