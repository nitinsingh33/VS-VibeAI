#!/bin/bash

# 🚀 Quick Railway Fix - Deploy Essential Files Only
echo "🔧 Fixing Railway deployment..."

# Create minimal deployment directory
mkdir -p railway-deploy
cd railway-deploy

# Copy only essential files
echo "📁 Copying essential files..."
cp ../main.py .
cp ../requirements.txt .
cp ../.env .
cp -r ../services/ .

# Create a simple Dockerfile for Railway
cat > Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y curl gcc g++ && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Create directories
RUN mkdir -p data exports logs static

# Set environment
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/api/health || exit 1

# Run app
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "$PORT", "--workers", "1"]
EOF

echo "✅ Essential files ready for deployment"
echo "📁 Contents:"
ls -la

# Try deploying from this clean directory
echo "🚀 Attempting Railway deployment..."
railway up

cd ..
echo "🎯 Deployment attempt completed!"
