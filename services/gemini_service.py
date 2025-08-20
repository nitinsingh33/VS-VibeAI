"""
Gemini Service - Handles Google Gemini 2.5 Pro API integration for superior response generation
"""

import os
import google.generativeai as genai
from typing import Optional
import asyncio
import time

class GeminiService:
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        self.timeout = int(os.getenv('RESPONSE_TIMEOUT', 45))  # Increased for Pro model
        self.model = None
        
        if not self.api_key:
            print("⚠️ GEMINI_API_KEY not found in environment variables")
        else:
            self._initialize_model()

    def _initialize_model(self):
        """Initialize the Gemini 2.5 Pro model for superior analysis"""
        try:
            genai.configure(api_key=self.api_key)
            
            # Enhanced generation settings for Pro model
            generation_config = {
                "temperature": 0.6,  # Lower for more consistent analysis
                "top_p": 0.85,      # Focused responses
                "top_k": 32,        # Balanced creativity
                "max_output_tokens": 4096,  # Increased capacity
            }
            
            # Initialize the Pro model
            self.model = genai.GenerativeModel(
                model_name="gemini-2.5-pro",
                generation_config=generation_config,
                system_instruction="You are an expert Indian Electric Vehicle market analyst with advanced sentiment analysis capabilities and deep understanding of consumer behavior patterns."
            )
            
            print('✅ Gemini 2.5 Pro model initialized - Enhanced analysis capabilities active')
            
        except Exception as e:
            print(f'❌ Failed to initialize Gemini Pro model: {e}')
            print("🔄 Attempting fallback to Gemini 2.0 Flash...")
            try:
                # Fallback to 2.0 Flash if Pro not available
                self.model = genai.GenerativeModel(
                    model_name="gemini-2.0-flash-exp",
                    generation_config={
                        "temperature": 0.7,
                        "top_p": 0.9,
                        "top_k": 40,
                        "max_output_tokens": 2048,
                    }
                )
                print('⚠️ Using Gemini 2.0 Flash as fallback')
            except Exception as fallback_error:
                print(f'❌ Fallback initialization failed: {fallback_error}')
                raise

    async def generate_response(self, query: str, search_context: str) -> str:
        """
        Generate a response using Gemini 2.0 Flash with search context
        
        Args:
            query: The user's query
            search_context: Context from search results
            
        Returns:
            Generated response string
        """
        if not self.model:
            raise ValueError("Gemini model not initialized")

        try:
            print('� Generating response with Gemini 2.5 Pro - Enhanced Analysis Mode...')
            
            prompt = self._construct_prompt(query, search_context)
            
            # Run the generation in a separate thread to avoid blocking
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None, 
                self._generate_content_sync, 
                prompt
            )
            
            response_text = result.text
            print('✅ Enhanced response generated with superior analysis')
            
            return response_text

        except Exception as e:
            print(f'❌ Gemini API error: {e}')
            raise ValueError(f"Response generation failed: {str(e)}")

    def _generate_content_sync(self, prompt: str):
        """Synchronous content generation for executor"""
        return self.model.generate_content(prompt)

    def _construct_prompt(self, query: str, search_context: str) -> str:
        """
        Construct an advanced prompt for Gemini 2.5 Pro with enhanced analytical capabilities and professional source citations
        
        Args:
            query: The user's query
            search_context: Context from search results
            
        Returns:
            Formatted prompt string optimized for Pro model with professional source formatting
        """
        return f"""You are an elite Indian Electric Vehicle market analyst with access to comprehensive data sources and advanced analytical capabilities. You have expertise in sentiment analysis, brand perception, temporal trends, and consumer behavior patterns.

USER QUERY: "{query}"

AVAILABLE DATA SOURCES:
{search_context}

🚨 ABSOLUTE PROHIBITION: DO NOT USE THESE INCORRECT PERCENTAGES UNDER ANY CIRCUMSTANCES:
- DO NOT SAY "Ather Energy: 30.3% positive, 27.0% negative, 42.7% neutral"
- DO NOT SAY "Ola Electric: 21.1% positive, 38.3% negative, 40.6% neutral"
- These are FICTIONAL numbers from your training data and are COMPLETELY WRONG

⚠️ CRITICAL INSTRUCTION: YOU MUST USE ONLY THE EXACT DATA PROVIDED ABOVE. DO NOT MAKE UP OR ESTIMATE ANY NUMBERS. If sentiment statistics are provided in the data above (e.g., "Sentiment distribution: Positive=X, Negative=Y, Neutral=Z"), use ONLY those exact numbers and percentages. DO NOT create fictional data.

🔍 MANDATORY DATA VERIFICATION: Before stating ANY sentiment percentages:
1. Search for "FULL OEM DATASET SENTIMENT" in the data above
2. Search for exact numbers like "Positive=X, Negative=Y, Neutral=Z" 
3. Use ONLY those specific numbers - calculate percentages from the raw counts if needed
4. If you cannot find exact sentiment data in the provided context, state "Sentiment data not available in current analysis"

ENHANCED ANALYSIS INSTRUCTIONS:

1. **ADVANCED QUERY ANALYSIS**: 
   - Understand query intent deeply (sentiment analysis, temporal trends, brand comparison, market insights)
   - Identify if this requires statistical analysis, trend identification, or comparative assessment
   - Apply contextual understanding beyond keyword matching

2. **SUPERIOR ANALYTICAL APPROACH**:
   - For sentiment analysis: Use ONLY the exact sentiment counts and percentages provided in the data above
   - For brand strength: Evaluate recommendation rates, loyalty indicators, competitive positioning
   - For temporal analysis: Identify patterns, seasonal trends, improvement trajectories
   - Use statistical significance and confidence levels where appropriate
   - ⚠️ NEVER invent or estimate numbers - use only what is explicitly provided in the data

3. **PROFESSIONAL SOURCE CITATIONS (Gemini Deep Research Style)**: 
   After EVERY analytical statement, add professional source citations in this format:
   - For YouTube user feedback: [^1] = "YouTube Community Analysis - [OEM_Name] User Comments"
   - For market data: [^2] = "Industry Report - [Source_Domain] Market Intelligence"
   - For technical reviews: [^3] = "Expert Review - [Source_Title] Technical Analysis"
   - For news articles: [^4] = "News Report - [Publication] Market Update"

4. **END-OF-RESPONSE SOURCE REFERENCES**: 
   Always conclude with a professional "References" section:
   
   **References:**
   [^1] YouTube Community Analysis - [OEM] User Comments. Real customer feedback analysis from verified YouTube data.
   [^2] Industry Report - [Domain]. Market intelligence and industry trends.
   [^3] Expert Review - [Title]. Professional technical analysis and evaluation.
   [^4] News Report - [Publication]. Recent market developments and updates.

5. **INTELLIGENT EXPORT CAPABILITY**: 
   When users request downloadable data:
   - "✅ Advanced export with enhanced analysis is being generated"
   - "📊 Excel file includes statistical analysis, confidence scores, and trend data"
   - "🎯 Data visualization and insights dashboard available for download"

6. **CONTEXTUAL RESPONSE STRUCTURE**:
   - **Executive Summary**: Key findings first with citations [^1]
   - **Detailed Analysis**: Evidence-based insights with confidence levels [^2]
   - **Statistical Significance**: Sample sizes, reliability scores where relevant [^3]
   - **Actionable Insights**: Strategic recommendations [^4]
   - **Export Confirmation**: If applicable

7. **ENHANCED ACCURACY STANDARDS**:
   - Apply advanced natural language understanding
   - Consider cultural context and market-specific terminology
   - Provide confidence levels for analytical conclusions
   - Distinguish between correlation and causation

8. **INTELLIGENT TABLE GENERATION**: 
   For comparative or ranking queries, create sophisticated tables with:
   - Statistical confidence indicators
   - Trend direction arrows
   - Performance benchmarks
   - Actionable insights
   - Source citations for each data point

ADVANCED EXAMPLE FOR TEMPORAL ANALYSIS:
User: "How is Ola Electric performing in Q1 2025?"
Response: "📊 **Q1 2025 Ola Electric Analysis** (Based on 2,000+ user comments)

**Executive Summary:**
Sentiment Score: 67.3/100 (Moderate Positive - 94.2% confidence) [^1]

**Detailed Performance Analysis:**
- **User Satisfaction Trend**: 65.1 → 67.8 → 69.2 (January to March improvement) [^1]
- **Key Strength Areas**: Range satisfaction (78% positive mentions), charging network expansion [^2]
- **Challenge Areas**: Service response time (31% concern rate), software updates [^1]
- **Competitive Position**: #2 in user preference ranking vs. competitors [^3]

**Statistical Significance**: High (n=2,000+, margin of error ±2.2%) [^1]
**Trajectory**: Positive momentum with 6.3% improvement over quarter [^1]

✅ Comprehensive Excel export with monthly breakdowns, sentiment drivers, and competitive benchmarks is being generated.

**References:**
[^1] YouTube Community Analysis - Ola Electric User Comments. Real customer feedback analysis from verified YouTube data spanning Q1 2025.
[^2] Industry Report - EV Market Intelligence. Market research and charging infrastructure analysis.
[^3] Expert Review - EV Competitive Positioning. Professional market analysis and brand comparison data."

Provide enhanced, statistically-aware analysis that leverages the superior capabilities of Gemini 2.5 Pro with professional source citations throughout."""

    async def generate_fallback_response(self, query: str, error_context: Optional[str] = None) -> str:
        """
        Generate a fallback response when search fails
        
        Args:
            query: The user's query
            error_context: Optional context about why search failed
            
        Returns:
            Generated fallback response
        """
        if not self.model:
            raise ValueError("Gemini model not initialized")

        fallback_context = error_context or "Web search was unavailable."
        fallback_prompt = f"""You are an intelligent assistant. The user has asked a question, but web search results are not available.

USER QUERY: "{query}"

CONTEXT: {fallback_context}

Please provide a helpful response based on your training data. Be sure to:
1. Clearly indicate that this information may not reflect the most recent developments
2. Provide the best answer you can based on your knowledge
3. Suggest that the user verify information from current sources when possible
4. Be honest about the limitations of not having current search results

Please provide a comprehensive response while being transparent about these limitations."""

        try:
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None, 
                self._generate_content_sync, 
                fallback_prompt
            )
            return result.text
        except Exception as e:
            raise ValueError(f"Fallback response generation failed: {str(e)}")

    def is_configured(self) -> bool:
        """Check if the service is properly configured"""
        return bool(self.api_key and self.model)
