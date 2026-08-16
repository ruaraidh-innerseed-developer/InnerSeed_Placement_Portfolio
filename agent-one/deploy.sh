#!/bin/bash

# Agent One Deployment Script
# Deploys Claude Agent One to systemd or Docker

set -e

echo "🚀 Agent One Deployment Script"
echo "=============================="

# Check Python version
python_version=$(python3 --version 2>&1 | grep -oP '\d+\.\d+')
echo "✅ Python $python_version found"

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Create directories
echo "📁 Creating necessary directories..."
mkdir -p logs temp cache

# Load environment
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cp .env.example .env
    echo "⚠️  Edit .env with your API keys and folder IDs before running!"
    exit 1
fi

# Ask deployment method
echo ""
echo "Choose deployment method:"
echo "1) Systemd Service (Linux)"
echo "2) Docker Container"
echo "3) Cron Job"
echo "4) Manual/Development (run once)"

read -p "Enter choice (1-4): " choice

case $choice in
    1)
        echo "📋 Setting up systemd service..."

        # Check if running as root
        if [ "$EUID" -ne 0 ]; then
            echo "⚠️  Systemd setup requires sudo. Running with sudo..."
            sudo bash -c "
                # Create agent-one user if doesn't exist
                id -u agent-one &>/dev/null || useradd -r -s /bin/bash agent-one

                # Copy service file
                cp agent-one.service /etc/systemd/system/
                systemctl daemon-reload

                # Set permissions
                chown -R agent-one:agent-one /opt/agent-one 2>/dev/null || true
            "
        fi

        echo "✅ Systemd service configured"
        echo ""
        echo "To start the service:"
        echo "  sudo systemctl start agent-one"
        echo "  sudo systemctl enable agent-one  (auto-start on reboot)"
        echo ""
        echo "To view logs:"
        echo "  sudo journalctl -u agent-one -f"
        ;;

    2)
        echo "🐳 Building Docker image..."
        docker build -t agent-one:latest .

        echo "✅ Docker image built"
        echo ""
        echo "To run the container:"
        echo "  docker run -d \\"
        echo "    --name agent-one \\"
        echo "    --env-file .env \\"
        echo "    -v \$(pwd)/logs:/app/logs \\"
        echo "    -v \$(pwd)/temp:/app/temp \\"
        echo "    agent-one:latest"
        echo ""
        echo "To view logs:"
        echo "  docker logs -f agent-one"
        ;;

    3)
        echo "⏰ Setting up cron job..."

        script_path=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
        cron_entry="*/30 * * * * cd $script_path && python -m src.claude_agent --mode once >> logs/cron.log 2>&1"

        # Add to crontab
        (crontab -l 2>/dev/null; echo "$cron_entry") | crontab -

        echo "✅ Cron job configured to run every 30 minutes"
        echo ""
        echo "To view cron logs:"
        echo "  tail -f logs/cron.log"
        echo ""
        echo "To modify cron job:"
        echo "  crontab -e"
        ;;

    4)
        echo "🚀 Starting Agent One in development mode..."
        python -m src.claude_agent --mode once
        echo "✅ Processing cycle complete"
        ;;

    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "🎉 Deployment complete!"
echo ""
echo "Next steps:"
echo "1. Verify all API keys in .env are set correctly"
echo "2. Create Google Drive folders (/Agent-One-Inbox/, etc.)"
echo "3. Get folder IDs from share links and add to .env"
echo "4. Upload a test video with brief to /Agent-One-Inbox/"
echo "5. Monitor logs to verify processing starts"
echo ""
echo "📖 For detailed docs, see: docs/DEPLOYMENT.md"
