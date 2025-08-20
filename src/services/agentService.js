import SearchService from './searchService.js';
import GeminiService from './geminiService.js';

class AgentService {
  constructor() {
    this.searchService = new SearchService();
    this.geminiService = new GeminiService();
  }

  async processQuery(query) {
    try {
      console.log(`🚀 Processing query: "${query}"`);
      const startTime = Date.now();

      // Step 1: Search for relevant information
      const searchResults = await this.searchService.search(query);
      
      if (searchResults.length === 0) {
        console.log('⚠️ No search results found, generating response from LLM knowledge only');
        return await this.generateFallbackResponse(query);
      }

      // Step 2: Extract context from search results
      const { context, sources } = this.searchService.extractSearchContext(searchResults);

      // Step 3: Generate response using Gemini with search context
      const response = await this.geminiService.generateResponse(query, context);

      const processingTime = Date.now() - startTime;
      console.log(`✅ Query processed successfully in ${processingTime}ms`);

      return {
        query,
        response,
        sources: sources.map(source => ({
          title: source.title,
          url: source.url,
          snippet: source.content
        })),
        searchResults: searchResults.length,
        processingTime,
        timestamp: new Date().toISOString()
      };

    } catch (error) {
      console.error('Agent processing error:', error.message);
      
      // Try to provide a fallback response if search fails
      if (error.message.includes('Search failed')) {
        console.log('🔄 Search failed, attempting fallback response...');
        return await this.generateFallbackResponse(query, error);
      }
      
      throw error;
    }
  }

  async generateFallbackResponse(query, originalError = null) {
    try {
      const fallbackContext = originalError 
        ? `Note: Web search was unavailable due to: ${originalError.message}. Please provide a response based on your training data and clearly indicate that this information may not reflect the most recent developments.`
        : `Note: No relevant search results were found. Please provide a response based on your training data and clearly indicate that this information may not reflect the most recent developments.`;

      const response = await this.geminiService.generateResponse(query, fallbackContext);

      return {
        query,
        response,
        sources: [],
        searchResults: 0,
        fallback: true,
        fallbackReason: originalError ? 'search_failed' : 'no_results',
        timestamp: new Date().toISOString()
      };

    } catch (fallbackError) {
      console.error('Fallback response generation failed:', fallbackError.message);
      throw new Error('Both search and fallback response generation failed');
    }
  }

  // Method to validate and sanitize queries
  validateQuery(query) {
    if (!query || typeof query !== 'string') {
      throw new Error('Query must be a non-empty string');
    }

    const trimmedQuery = query.trim();
    if (trimmedQuery.length === 0) {
      throw new Error('Query cannot be empty');
    }

    if (trimmedQuery.length > 500) {
      throw new Error('Query is too long (maximum 500 characters)');
    }

    return trimmedQuery;
  }

  // Method to get service health status
  getHealthStatus() {
    return {
      searchService: {
        configured: !!process.env.SERPER_API_KEY,
        status: 'ready'
      },
      geminiService: {
        configured: !!process.env.GEMINI_API_KEY,
        status: 'ready'
      },
      timestamp: new Date().toISOString()
    };
  }
}

export default AgentService;
