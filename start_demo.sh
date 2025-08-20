#!/bin/bash

# SolysAI Demo Launcher
# Starts all demo services with proper configuration

echo "🚀 Starting SolysAI Demo Platform..."
echo "======================================"

# Kill any existing processes
echo "🧹 Cleaning up existing processes..."
pkill -f "streamlit\|python.*main.py" 2>/dev/null || true
lsof -ti:8000,8501,8503 | xargs kill -9 2>/dev/null || true

sleep 2

# Start FastAPI backend
echo "🔧 Starting SolysAI API Backend (Port 8000)..."
python3 main.py &
BACKEND_PID=$!

sleep 3

# Start Streamlit Premium Interface
echo "🎨 Starting SolysAI Premium Interface (Port 8501)..."
streamlit run streamlit_app_premium.py --server.port=8501 --server.address=0.0.0.0 &
STREAMLIT_PID=$!

sleep 3

# Start Analytics Dashboard
echo "📊 Starting SolysAI Analytics Dashboard (Port 8503)..."
streamlit run analytics_dashboard.py --server.port=8503 --server.address=0.0.0.0 &
ANALYTICS_PID=$!

sleep 5

# Check services
echo "🔍 Checking service status..."

if curl -s http://localhost:8000/api/health > /dev/null; then
    echo "✅ API Backend: RUNNING (http://localhost:8000)"
else
    echo "❌ API Backend: FAILED"
fi

if curl -s -I http://localhost:8501 > /dev/null; then
    echo "✅ Premium Interface: RUNNING (http://localhost:8501)"
else
    echo "❌ Premium Interface: FAILED"
fi

if curl -s -I http://localhost:8503 > /dev/null; then
    echo "✅ Analytics Dashboard: RUNNING (http://localhost:8503)"
else
    echo "❌ Analytics Dashboard: FAILED"
fi

echo ""
echo "🎯 DEMO READY!"
echo "======================================"
echo "📱 Main Platform:    http://localhost:8501"
echo "📊 Analytics:        http://localhost:8503"
echo "🔧 API Docs:         http://localhost:8000/docs"
echo "❤️  Health Check:    http://localhost:8000/api/health"
echo ""
echo "📈 Dataset: 7,443 real YouTube comments"
echo "🏢 OEMs: Ola Electric, TVS iQube, Bajaj Chetak, Ather, Hero Vida"
echo "🎨 Platform: SolysAI (Fully Rebranded)"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for interrupt
trap 'echo "🛑 Stopping services..."; kill $BACKEND_PID $STREAMLIT_PID $ANALYTICS_PID; exit' INT
wait
