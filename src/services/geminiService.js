import { GoogleGenerativeAI } from '@google/generative-ai';

class GeminiService {
  constructor() {
    this.apiKey = process.env.GEMINI_API_KEY;
    this.timeout = parseInt(process.env.RESPONSE_TIMEOUT) || 30000;
    this.genAI = null;
    this.model = null;
    this.initializeModel();
  }

  initializeModel() {
    if (!this.apiKey) {
      throw new Error('GEMINI_API_KEY not configured');
    }

    try {
      this.genAI = new GoogleGenerativeAI(this.apiKey);
      this.model = this.genAI.getGenerativeModel({ 
        model: "gemini-2.5-pro",
        generationConfig: {
          temperature: 0.6,
          topP: 0.85,
          topK: 32,
          maxOutputTokens: 4096,
        }
      });
      console.log('✅ Gemini 2.5 Pro model initialized');
    } catch (error) {
      console.error('Failed to initialize Gemini model:', error.message);
      throw error;
    }
  }

  async generateResponse(query, searchContext) {
    if (!this.model) {
      throw new Error('Gemini model not initialized');
    }

    try {
      console.log('🤖 Generating response with Gemini 2.0 Flash...');

      const prompt = this.constructPrompt(query, searchContext);
      
      const result = await Promise.race([
        this.model.generateContent(prompt),
        new Promise((_, reject) => 
          setTimeout(() => reject(new Error('Gemini API timeout')), this.timeout)
        )
      ]);

      const response = result.response;
      const text = response.text();

      console.log('✅ Response generated successfully');
      return text;

    } catch (error) {
      console.error('Gemini API error:', error.message);
      throw new Error(`Response generation failed: ${error.message}`);
    }
  }

  constructPrompt(query, searchContext) {
    return `You are an intelligent research assistant. Your task is to provide a comprehensive, factually accurate response to the user's query by combining the latest information from web search results with your existing knowledge.

USER QUERY: "${query}"

RECENT SEARCH RESULTS:
${searchContext}

INSTRUCTIONS:
1. Analyze the search results and identify the most relevant and recent information
2. Combine this information with your existing knowledge to provide a comprehensive answer
3. Prioritize factual accuracy and cite specific information from the search results when relevant
4. If there are conflicting information sources, acknowledge this and explain the different perspectives
5. Structure your response clearly with proper formatting
6. Be conversational but authoritative in your tone
7. If the search results don't contain sufficient information to answer the query, supplement with your general knowledge while being clear about what comes from search vs. your training data

Please provide a well-structured, informative response that addresses the user's query comprehensively.`;
  }

  // Alternative method for streaming responses (if needed in the future)
  async generateStreamingResponse(query, searchContext) {
    if (!this.model) {
      throw new Error('Gemini model not initialized');
    }

    try {
      const prompt = this.constructPrompt(query, searchContext);
      const result = await this.model.generateContentStream(prompt);
      
      return result.stream;
    } catch (error) {
      console.error('Gemini streaming error:', error.message);
      throw new Error(`Streaming response generation failed: ${error.message}`);
    }
  }
}

export default GeminiService;
