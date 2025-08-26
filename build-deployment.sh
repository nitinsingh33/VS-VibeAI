#!/bin/bash

# VibeAI Deployment Builder
echo "🚀 Building VibeAI Deployment Package..."

# Create deployment directory structure
mkdir -p deployment/{backend,frontend,analytics,premium,proxy,nginx}
mkdir -p deployment/data/{json,exports,logs}
mkdir -p deployment/config

# Copy application files
echo "📁 Organizing application files..."

# Backend files
cp main.py deployment/backend/
cp -r services/ deployment/backend/
cp requirements.txt deployment/backend/
cp .env deployment/backend/
cp Dockerfile deployment/backend/

# Frontend files
cp -r web/* deployment/frontend/
cp web/Dockerfile.frontend deployment/frontend/Dockerfile

# Analytics files
cp analytics_dashboard.py deployment/analytics/
cp streamlit_app_premium.py deployment/premium/
cp Dockerfile.streamlit deployment/analytics/
cp Dockerfile.streamlit-premium deployment/premium/

# Nginx files
cp -r nginx/ deployment/
cp docker-compose.yml deployment/

# Essential data files (latest comments)
echo "📊 Copying latest data files..."
cp all_oem_comments_historical_*.json deployment/data/json/ 2>/dev/null || true
cp comments_*_2025_*.json deployment/data/json/ 2>/dev/null || true

# Create deployment scripts
cat > deployment/deploy.sh << 'EOF'
#!/bin/bash

echo "🚀 Starting VibeAI Deployment..."

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose not found. Please install Docker Compose first."
    exit 1
fi

# Build and start services
echo "🔨 Building Docker containers..."
docker-compose down
docker-compose build --no-cache

echo "🎯 Starting VibeAI services..."
docker-compose up -d

echo "⏳ Waiting for services to start..."
sleep 30

# Health checks
echo "🏥 Performing health checks..."
echo "Backend: $(curl -s http://localhost:8000/api/health | jq -r '.status' 2>/dev/null || echo 'Failed')"
echo "Analytics: $(curl -s http://localhost:8501/_stcore/health | head -1 2>/dev/null || echo 'Failed')"
echo "Premium: $(curl -s http://localhost:8502/_stcore/health | head -1 2>/dev/null || echo 'Failed')"
echo "Frontend: $(curl -s http://localhost:5173 | head -1 2>/dev/null || echo 'Failed')"

echo ""
echo "🎉 VibeAI Deployment Complete!"
echo ""
echo "📊 Access your services:"
echo "🖥️  Frontend:        http://localhost:5173"
echo "⚡ Backend API:     http://localhost:8000"
echo "📈 Analytics:       http://localhost:8501"
echo "💎 Premium:         http://localhost:8502"
echo "🌐 Full Stack:      http://localhost:80 (Nginx)"
echo ""
echo "📖 API Documentation: http://localhost:8000/docs"
echo "🏥 Health Check:      http://localhost:8000/api/health"
EOF

chmod +x deployment/deploy.sh

# Create production deployment script
cat > deployment/deploy-production.sh << 'EOF'
#!/bin/bash

echo "🚀 Starting VibeAI Production Deployment..."

# Set production environment
export NODE_ENV=production
export PYTHONOPTIMIZE=1

# Build production images
echo "🔨 Building production Docker containers..."
docker-compose -f docker-compose.yml -f docker-compose.prod.yml down
docker-compose -f docker-compose.yml -f docker-compose.prod.yml build --no-cache

echo "🎯 Starting VibeAI production services..."
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

echo "⏳ Waiting for services to initialize..."
sleep 45

echo "🎉 VibeAI Production Deployment Complete!"
echo ""
echo "🌐 Production Access:"
echo "Main Application: http://your-domain.com"
echo "API Endpoint:     http://your-domain.com/api"
echo "Analytics:        http://your-domain.com/analytics"
echo "Premium:          http://your-domain.com/premium"
EOF

chmod +x deployment/deploy-production.sh

# Create environment template
cat > deployment/.env.template << 'EOF'
# VibeAI Environment Configuration

# API Keys (Required)
SERPER_API_KEY=your_serper_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
YOUTUBE_API_KEY=your_youtube_api_key_here

# Application Settings
PORT=8000
MAX_SEARCH_RESULTS=5
SEARCH_TIMEOUT=10
RESPONSE_TIMEOUT=120

# Database (Optional - for advanced deployments)
# DATABASE_URL=postgresql://user:password@localhost:5432/vibeai

# Security (Production)
# SECRET_KEY=your_secret_key_here
# ALLOWED_HOSTS=your-domain.com,www.your-domain.com

# External Services (Optional)
# REDIS_URL=redis://localhost:6379
# ELASTICSEARCH_URL=http://localhost:9200
EOF

# Create requirements for deployment
cat > deployment/requirements-deploy.txt << 'EOF'
# Deployment Requirements
docker>=6.0.0
docker-compose>=2.0.0

# Optional: Cloud deployment tools
# aws-cli>=2.0.0
# gcloud>=400.0.0
# azure-cli>=2.0.0
EOF

echo "✅ Deployment package created successfully!"
echo ""
echo "📁 Structure created:"
echo "deployment/"
echo "├── backend/           # FastAPI backend"
echo "├── frontend/          # React frontend"
echo "├── analytics/         # Streamlit analytics"
echo "├── premium/           # Streamlit premium"
echo "├── nginx/             # Reverse proxy"
echo "├── data/              # Application data"
echo "├── docker-compose.yml # Container orchestration"
echo "├── deploy.sh          # Development deployment"
echo "├── deploy-production.sh # Production deployment"
echo "└── .env.template      # Environment template"
echo ""
echo "🚀 Next steps:"
echo "1. cd deployment/"
echo "2. cp .env.template .env"
echo "3. Edit .env with your API keys"
echo "4. ./deploy.sh"
