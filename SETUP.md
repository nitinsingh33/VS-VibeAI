# VibeAI Search Agent - Setup Guide

## Quick Start

Follow these steps to get your VibeAI Search Agent up and running:

### 1. Install Dependencies

```bash
pip install fastapi uvicorn python-dotenv requests google-generativeai python-multipart
```

### 2. Get API Keys

#### Serper API (Google Search)
1. Visit https://serper.dev/
2. Sign up for a free account
3. Get your API key from the dashboard
4. Free tier: 2,500 searches/month

#### Google Gemini API
1. Visit https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Create a new API key
4. Free tier: Generous usage limits

### 3. Configure Environment

Create a `.env` file in the project root:

```env
SERPER_API_KEY=your_serper_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
PORT=8000
```

### 4. Test the Setup

```bash
python3 test.py
```

### 5. Run the Agent

Choose your preferred interface:

#### Web Interface (Recommended)
```bash
python3 main.py
```
Then visit: http://localhost:8000

#### Command Line Interface
```bash
python3 cli.py
```

#### Programmatic Usage
```bash
python3 example.py
```

## API Usage Examples

### Python Requests
```python
import requests

response = requests.post('http://localhost:8000/api/search', 
    json={'query': 'What are the latest AI developments?'})
result = response.json()
print(result['response'])
```

### cURL
```bash
curl -X POST "http://localhost:8000/api/search" \
     -H "Content-Type: application/json" \
     -d '{"query": "What is machine learning?"}'
```

### JavaScript/Fetch
```javascript
const response = await fetch('http://localhost:8000/api/search', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({query: 'Explain quantum computing'})
});
const result = await response.json();
console.log(result.response);
```

## Architecture Overview

### Components
- **FastAPI Server** (`main.py`): REST API and web interface
- **Agent Service** (`services/agent_service.py`): Main orchestrator
- **Search Service** (`services/search_service.py`): Serper API integration
- **Gemini Service** (`services/gemini_service.py`): AI response generation

### Data Flow
1. User submits query → Agent Service
2. Agent Service → Search Service (Serper API)
3. Search results → Gemini Service (AI processing)
4. Generated response → User with sources

## Configuration Options

### Environment Variables
```env
# Required
SERPER_API_KEY=your_key_here
GEMINI_API_KEY=your_key_here

# Optional
PORT=8000                    # Server port
MAX_SEARCH_RESULTS=5         # Max search results to use
SEARCH_TIMEOUT=10            # Search timeout (seconds)
RESPONSE_TIMEOUT=30          # AI response timeout (seconds)
```

### Service Configuration
```python
# Custom configuration example
from services.agent_service import AgentService

agent = AgentService()
result = await agent.process_query(
    query="Your question here",
    max_results=3  # Override default
)
```

## Error Handling

The agent includes robust error handling:

- **Search failures**: Falls back to LLM-only responses
- **API timeouts**: Configurable timeout limits
- **Invalid queries**: Input validation and sanitization
- **Rate limits**: Graceful handling of API limits

## Performance Tips

1. **Optimize search results**: Use `max_results` parameter to limit API calls
2. **Cache responses**: Consider implementing response caching for repeated queries
3. **Batch processing**: Use the programmatic interface for multiple queries
4. **Monitor usage**: Track API usage to stay within limits

## Troubleshooting

### Common Issues

**"Import could not be resolved"**
```bash
pip install fastapi uvicorn python-dotenv requests google-generativeai
```

**"API key not configured"**
- Check your `.env` file exists and has valid keys
- Ensure no extra spaces around the `=` sign

**"Search failed"**
- Verify SERPER_API_KEY is correct
- Check your API quota at https://serper.dev/dashboard

**"Response generation failed"**
- Verify GEMINI_API_KEY is correct
- Check your Google AI Studio quota

### Debug Mode
Set `DEBUG=1` environment variable for detailed logging:
```bash
DEBUG=1 python3 main.py
```

## Production Deployment

### Using Gunicorn
```bash
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Docker Deployment
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Security
- Never commit `.env` files to version control
- Use environment variables in production
- Consider using secret management services

## API Reference

### POST /api/search
**Request:**
```json
{
  "query": "string (required, 1-500 chars)",
  "max_results": "integer (optional, 1-10, default: 5)"
}
```

**Response:**
```json
{
  "query": "string",
  "response": "string",
  "sources": [
    {
      "title": "string",
      "url": "string", 
      "snippet": "string"
    }
  ],
  "search_results": "integer",
  "processing_time": "float",
  "timestamp": "string",
  "fallback": "boolean (optional)",
  "fallback_reason": "string (optional)"
}
```

### GET /api/health
**Response:**
```json
{
  "status": "healthy",
  "timestamp": "string",
  "services": {
    "search_service": {"configured": true, "status": "ready"},
    "gemini_service": {"configured": true, "status": "ready"}
  }
}
```

## Support

For issues and questions:
1. Check this setup guide
2. Review the error messages carefully
3. Verify your API keys and quotas
4. Check the troubleshooting section
