FROM python:3.11-slim

# Install system dependencies (FFmpeg is critical for video processing)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create necessary directories
RUN mkdir -p logs temp cache

# Run Agent One in scheduled mode (every 30 minutes)
CMD ["python", "-m", "src.claude_agent", "--mode", "scheduled", "--interval", "30"]
