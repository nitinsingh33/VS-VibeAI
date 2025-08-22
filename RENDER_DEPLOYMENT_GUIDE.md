# 🚀 SolysAI Sentiment Analysis - Render Deployment Guide

## 📋 Prerequisites

Before deploying to Render, ensure you have:
1. A Render account (free tier available)
2. Your GitHub repository pushed to GitHub
3. API keys for:
   - **Serper API Key** (for web search functionality)
   - **Gemini API Key** (for AI responses)

## 🔧 API Keys Setup

### Get Serper API Key:
1. Go to [serper.dev](https://serper.dev)
2. Sign up for a free account
3. Get your API key from the dashboard

### Get Gemini API Key:
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the generated key

## 🚀 Deployment Steps

### Step 1: Push to GitHub
```bash
# Add all files
git add .

# Commit changes
git commit -m "Deploy to Render: Add sentiment analysis app"

# Push to GitHub
git push origin main
```

### Step 2: Deploy on Render

1. **Go to Render Dashboard**
   - Visit [render.com](https://render.com)
   - Sign in with your GitHub account

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select this repository

3. **Configure Deployment Settings**
   ```
   Name: solysai-sentiment-analysis
   Region: Oregon (US West)
   Branch: main
   Root Directory: (leave blank)
   Runtime: Python 3
   Build Command: ./build.sh
   Start Command: python production_app.py
   Plan: Free (or Starter for better performance)
   ```

4. **Set Environment Variables**
   In the Render dashboard, add these environment variables:
   ```
   SERPER_API_KEY=your_serper_api_key_here
   GEMINI_API_KEY=your_gemini_api_key_here
   PORT=8000
   ENVIRONMENT=production
   PYTHONPATH=.
   MAX_SEARCH_RESULTS=5
   SEARCH_TIMEOUT=10000
   RESPONSE_TIMEOUT=30000
   ```

5. **Deploy**
   - Click "Create Web Service"
   - Wait for the build to complete (5-10 minutes)

## 🔗 URLs After Deployment

Once deployed, your app will be available at:
- **Main App**: `https://your-app-name.onrender.com`
- **Health Check**: `https://your-app-name.onrender.com/health`
- **API Docs**: `https://your-app-name.onrender.com/docs`
- **Sentiment API**: `https://your-app-name.onrender.com/api/enhanced-search`

## 🧪 Testing Your Deployment

### 1. Health Check
```bash
curl https://your-app-name.onrender.com/health
```

### 2. Test Sentiment Analysis
```bash
curl -X POST "https://your-app-name.onrender.com/api/enhanced-search" \
  -H "Content-Type: application/json" \
  -d '{"query": "What do people think about Ola Electric scooters?", "use_youtube_data": true}'
```

### 3. Test Production Optimizer
```python
import requests

# Test the optimized sentiment classifier
response = requests.post(
    "https://your-app-name.onrender.com/api/enhanced-search",
    json={
        "query": "Analyze sentiment for Ola Electric reviews",
        "use_youtube_data": True,
        "max_search_results": 5
    }
)

print(response.json())
```

## 📊 Features Available After Deployment

1. **Sentiment Analysis API** - Analyze text sentiment with emoji context
2. **Production Speed Optimizer** - 4x faster processing with caching
3. **Multi-language Support** - Hindi, English, and mixed language analysis
4. **Real-time Processing** - Handle multiple requests concurrently
5. **Health Monitoring** - Built-in health checks and error handling
6. **Export Functionality** - Generate Excel, Word, and CSV reports

## 🔧 Configuration Options

### Environment Variables
```bash
# Required
SERPER_API_KEY=your_key_here
GEMINI_API_KEY=your_key_here

# Optional
PORT=8000                    # Server port
MAX_SEARCH_RESULTS=5         # Maximum search results
SEARCH_TIMEOUT=10000         # Search timeout in ms
RESPONSE_TIMEOUT=30000       # Response timeout in ms
ENVIRONMENT=production       # Environment mode
PYTHONPATH=.                 # Python path
```

### Performance Tuning
For better performance on paid Render plans:
- Increase worker count in `gunicorn.conf.py`
- Enable caching in production settings
- Use higher memory limits

## 🐛 Troubleshooting

### Common Issues:

1. **Build Fails**
   - Check `requirements.txt` is correct
   - Ensure `build.sh` is executable
   - Check logs in Render dashboard

2. **App Won't Start**
   - Verify environment variables are set
   - Check Python version compatibility
   - Review startup logs

3. **API Errors**
   - Ensure API keys are correct
   - Check CORS settings for frontend integration
   - Verify endpoint URLs

4. **Performance Issues**
   - Use production optimizer (`ProductionSentimentOptimizer`)
   - Enable caching for repeated requests
   - Consider upgrading Render plan

### Log Access:
- View logs in Render dashboard under "Logs" tab
- Use `/health` endpoint to check service status
- Monitor response times and error rates

## 📈 Performance Optimization

Your deployed app includes several optimizations:

1. **Caching Layer** - 74% cache hit rate for repeated content
2. **Fast Classification** - Instant classification for obvious patterns
3. **Batch Processing** - Handle multiple requests efficiently
4. **Production Logging** - Comprehensive error tracking
5. **Health Monitoring** - Automatic health checks

## 🔒 Security Features

- CORS protection for cross-origin requests
- Trusted host middleware
- Environment variable protection
- Error handling without sensitive data exposure
- Production-safe logging

## 📞 Support

If you encounter issues:
1. Check the Render logs first
2. Verify all environment variables are set
3. Test endpoints using the `/health` check
4. Review the API documentation at `/docs`

## 🎯 Next Steps

After successful deployment:
1. Test all API endpoints
2. Configure your frontend to use the new URL
3. Set up monitoring and alerts
4. Consider adding a custom domain
5. Monitor performance and optimize as needed

## 💡 Cost Optimization

- **Free Tier**: Good for testing and development
- **Starter Plan ($7/month)**: Better performance and uptime
- **Standard Plan**: For production workloads

Choose based on your usage requirements and performance needs.

---

🎉 **Congratulations!** Your SolysAI Sentiment Analysis app is now deployed and ready for production use!

**Live URL**: Replace `your-app-name` with your actual Render app name
**API Endpoint**: `https://your-app-name.onrender.com/api/enhanced-search`
