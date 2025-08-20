import axios from 'axios';

class SearchService {
  constructor() {
    this.apiKey = process.env.SERPER_API_KEY;
    this.baseUrl = 'https://google.serper.dev/search';
    this.maxResults = parseInt(process.env.MAX_SEARCH_RESULTS) || 5;
    this.timeout = parseInt(process.env.SEARCH_TIMEOUT) || 10000;
  }

  async search(query) {
    if (!this.apiKey) {
      throw new Error('SERPER_API_KEY not configured');
    }

    try {
      console.log(`🔍 Searching for: "${query}"`);
      
      const response = await axios.post(
        this.baseUrl,
        {
          q: query,
          num: this.maxResults,
          hl: 'en',
          gl: 'us'
        },
        {
          headers: {
            'X-API-KEY': this.apiKey,
            'Content-Type': 'application/json'
          },
          timeout: this.timeout
        }
      );

      const results = this.formatSearchResults(response.data);
      console.log(`✅ Found ${results.length} search results`);
      
      return results;
    } catch (error) {
      console.error('Search API error:', error.message);
      if (error.response) {
        console.error('Response status:', error.response.status);
        console.error('Response data:', error.response.data);
      }
      throw new Error(`Search failed: ${error.message}`);
    }
  }

  formatSearchResults(data) {
    const results = [];

    // Process organic results
    if (data.organic) {
      data.organic.forEach(result => {
        results.push({
          title: result.title,
          url: result.link,
          snippet: result.snippet,
          source: 'organic'
        });
      });
    }

    // Process featured snippet if available
    if (data.answerBox) {
      results.unshift({
        title: data.answerBox.title || 'Featured Snippet',
        url: data.answerBox.link,
        snippet: data.answerBox.snippet || data.answerBox.answer,
        source: 'featured'
      });
    }

    // Process knowledge graph if available
    if (data.knowledgeGraph) {
      results.unshift({
        title: data.knowledgeGraph.title,
        url: data.knowledgeGraph.website || data.knowledgeGraph.source?.url,
        snippet: data.knowledgeGraph.description,
        source: 'knowledge_graph'
      });
    }

    return results.slice(0, this.maxResults);
  }

  // Helper method to extract key information from search results
  extractSearchContext(results) {
    const context = results.map(result => ({
      title: result.title,
      content: result.snippet,
      url: result.url
    }));

    const combinedContext = context
      .map(item => `Title: ${item.title}\nContent: ${item.content}\nSource: ${item.url}`)
      .join('\n\n---\n\n');

    return {
      context: combinedContext,
      sources: context
    };
  }
}

export default SearchService;
