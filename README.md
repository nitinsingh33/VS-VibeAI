# VibeAI Search Agent (Python)

An intelligent Python agent that searches for information using Google/Serper API and generates factually grounded responses using Gemini 2.0 Flash.

## Features

- Real-time web search using Serper API
- AI-powered response generation with Gemini 2.0 Flash
- Combines search results with LLM knowledge for factually grounded responses
- Provides source URLs for transparency
- FastAPI-based RESTful API interface
- Command-line interface for direct interaction
- Web interface for easy interaction

## Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file with your API keys:
```
SERPER_API_KEY=your_serper_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
PORT=8000
```

3. Get API Keys:
   - **Serper API**: Sign up at https://serper.dev/ for Google search API
   - **Gemini API**: Get your key from https://makersuite.google.com/app/apikey

## Usage

### Start the FastAPI server:
```bash
python main.py
```

### Use the command-line interface:
```bash
python cli.py "What are the latest developments in AI?"
```

### API Endpoints

#### POST /api/search
Search and generate response based on a query.

**Request:**
```json
{
  "query": "What are the latest developments in AI?",
  "max_results": 5
}
```

**Response:**
```json
{
  "query": "What are the latest developments in AI?",
  "response": "Based on recent search results and current knowledge...",
  "sources": [
    {
      "title": "Article Title",
      "url": "https://example.com",
      "snippet": "Article snippet..."
    }
  ],
  "search_results": 5,
  "processing_time": 1234.56,
  "timestamp": "2025-08-15T...",
  "fallback": false
}
```

#### GET /api/health
Check the health status of all services.

### Command Line Interface

The CLI provides an easy way to interact with the agent directly:

```bash
# Interactive mode
python cli.py

# Single query
python cli.py "What are the latest developments in AI?"

# Help
python cli.py --help
```

### Testing

Run the test script to verify everything is working:

```bash
python test.py
```

## Architecture

- `main.py` - FastAPI server and web interface
- `cli.py` - Command-line interface
- `test.py` - Test script
- `services/agent_service.py` - Main orchestrator
- `services/search_service.py` - Handles Serper API integration
- `services/gemini_service.py` - Handles Gemini AI integration
- `requirements.txt` - Python dependencies

## Features in Detail

### 🔍 Smart Search Integration
- Uses Serper API for real-time Google search
- Processes multiple result types (organic, featured snippets, knowledge graph)
- Intelligent result ranking and filtering

### 🤖 Advanced AI Response Generation
- Powered by Gemini 2.0 Flash for cutting-edge AI capabilities
- Combines search results with LLM knowledge
- Fallback responses when search is unavailable
- Configurable generation parameters

### 📚 Source Attribution
- Provides clickable source URLs
- Shows article titles and snippets
- Transparent information sourcing
- Helps users verify information

### 🌐 Multiple Interfaces
- **Web Interface**: User-friendly browser interface
- **REST API**: For integration with other applications
- **CLI**: Command-line tool for developers and automation

### ⚡ Performance & Reliability
- Async processing for better performance
- Error handling and fallback mechanisms
- Configurable timeouts and limits
- Health monitoring endpoints

## Getting API Keys

### Serper API (Google Search)
1. Visit https://serper.dev/
2. Sign up for a free account
3. Get your API key from the dashboard
4. Free tier includes 2,500 searches per month

### Google Gemini API
1. Visit https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Create a new API key
4. Free tier includes generous usage limits

## Environment Configuration

Create a `.env` file in the project root:

```env
# Required API Keys
SERPER_API_KEY=your_serper_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here

# Optional Configuration
PORT=8000
MAX_SEARCH_RESULTS=5
SEARCH_TIMEOUT=10
RESPONSE_TIMEOUT=30
```

## Troubleshooting

### Common Issues

1. **Import errors when running**
   ```bash
   pip install -r requirements.txt
   ```

2. **API key not found**
   - Check your `.env` file exists and has the correct keys
   - Verify API keys are valid and active

3. **Search failures**
   - Verify SERPER_API_KEY is correct
   - Check if you've exceeded API limits
   - The agent will fall back to LLM-only responses

4. **Gemini API errors**
   - Verify GEMINI_API_KEY is correct
   - Check API quota and billing status
   - Try reducing response timeout if requests are timing out

### Debug Mode

Run with debug logging:
```bash
export DEBUG=1
python main.py
```
# SolysAI_Agent
