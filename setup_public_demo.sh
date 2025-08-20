#!/bin/bash

# SolysAI Public Demo Setup with Ngrok
# Makes the demo accessible over the internet

echo "🌐 Setting up SolysAI for Public Access..."
echo "========================================"

# Check if ngrok is installed
if ! command -v ngrok &> /dev/null; then
    echo "❌ Ngrok not found. Installing..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &> /dev/null; then
            brew install ngrok
        else
            echo "Please install Homebrew first: https://brew.sh/"
            exit 1
        fi
    else
        echo "Please install ngrok from: https://ngrok.com/download"
        exit 1
    fi
fi

# Start local services first
echo "🚀 Starting local services..."
./start_demo.sh &
LOCAL_DEMO_PID=$!

sleep 10

# Create ngrok tunnel for main platform
echo "🔗 Creating public tunnel for SolysAI Platform..."
ngrok http 8501 --log=stdout > ngrok_platform.log &
NGROK_PLATFORM_PID=$!

sleep 5

# Create ngrok tunnel for analytics
echo "📊 Creating public tunnel for Analytics Dashboard..."
ngrok http 8503 --log=stdout > ngrok_analytics.log &
NGROK_ANALYTICS_PID=$!

sleep 5

# Create ngrok tunnel for API
echo "🔧 Creating public tunnel for API..."
ngrok http 8000 --log=stdout > ngrok_api.log &
NGROK_API_PID=$!

sleep 5

# Extract URLs from ngrok logs
echo "🌐 Public URLs:"
echo "==============="

PLATFORM_URL=$(curl -s localhost:4040/api/tunnels | jq -r '.tunnels[] | select(.config.addr=="http://localhost:8501") | .public_url')
ANALYTICS_URL=$(curl -s localhost:4041/api/tunnels | jq -r '.tunnels[] | select(.config.addr=="http://localhost:8503") | .public_url')
API_URL=$(curl -s localhost:4042/api/tunnels | jq -r '.tunnels[] | select(.config.addr=="http://localhost:8000") | .public_url')

echo "🎨 SolysAI Platform:     $PLATFORM_URL"
echo "📊 Analytics Dashboard:  $ANALYTICS_URL"  
echo "🔧 API Documentation:    $API_URL/docs"
echo ""
echo "🎯 Share these URLs for public demo access!"
echo ""
echo "Press Ctrl+C to stop all services and tunnels"

# Cleanup function
cleanup() {
    echo "🛑 Stopping all services..."
    kill $LOCAL_DEMO_PID $NGROK_PLATFORM_PID $NGROK_ANALYTICS_PID $NGROK_API_PID 2>/dev/null
    rm -f ngrok_*.log
    exit
}

trap cleanup INT
wait
