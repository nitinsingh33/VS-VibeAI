"""
Enhanced Sentiment Analysis Service - Advanced AI-powered comment classification
Addresses: Sarcasm detection, Context understanding, Multilingual support
"""

import re
import json
import os
import time
from typing import Dict, List, Any, Optional, Tuple
import google.generativeai as genai
from collections import defaultdict
import asyncio
from .advanced_sentiment_classifier import AdvancedSentimentClassifier

class EnhancedSentimentAnalyzer:
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        self.gemini_model = None
        self._initialize_gemini()
        
        # Initialize the new advanced classifier
        self.advanced_classifier = AdvancedSentimentClassifier()
        print("✅ Advanced multi-layer sentiment classifier initialized")
        
        # Legacy patterns for backward compatibility
        self.sarcasm_indicators = {
            'punctuation_patterns': [
                r'!{2,}',  # Multiple exclamation marks
                r'\?{2,}',  # Multiple question marks
                r'\.{3,}',  # Ellipsis overuse
                r'[!?]{3,}',  # Mixed excessive punctuation
            ],
            'phrase_patterns': [
                r'oh (really|wow|great)',
                r'(sure|yeah) (right|sure)',
                r'totally (not|the best)',
                r'(amazing|wonderful|perfect) service',  # Often sarcastic in complaint context
                r'best (decision|purchase) ever',
                r'couldn\'t be (better|worse)',
                r'love (spending|wasting)',
                r'thanks for (nothing|the headache)',
            ],
            'contradictory_patterns': [
                r'(great|good|excellent).*(but|however|unfortunately)',
                r'(love|like).*(except|but|unfortunately)',
                r'(perfect|amazing).*(if only|wish|except)',
            ]
        }
        
        # Context detection for product relevance
        self.product_contexts = {
            'electric_vehicle_terms': [
                'scooter', 'bike', 'vehicle', 'ev', 'electric', 'battery', 'charging', 
                'range', 'mileage', 'speed', 'acceleration', 'motor', 'ride', 'driving',
                'ola', 'ather', 'bajaj', 'tvs', 'hero', 'revolt', 'ultraviolette', 
                'bgauss', 'river', 'ampere', 'chetak', 'iqube', 'vida', 's1', '450x'
            ],
            'service_terms': [
                'service', 'support', 'center', 'maintenance', 'repair', 'warranty',
                'technician', 'mechanic', 'booking', 'appointment', 'staff', 'help'
            ],
            'experience_terms': [
                'experience', 'journey', 'ownership', 'usage', 'daily', 'commute',
                'travel', 'trip', 'performance', 'comfort', 'satisfaction'
            ]
        }
        
        # Multilingual patterns (Hindi-English mixed)
        self.multilingual_patterns = {
            'hindi_positive': {
                'अच्छा': 'good', 'बेहतरीन': 'excellent', 'शानदार': 'amazing',
                'बढ़िया': 'great', 'सुपर': 'super', 'जबरदस्त': 'awesome',
                'मस्त': 'nice', 'धांसू': 'cool', 'कमाल': 'wonderful'
            },
            'hindi_negative': {
                'बुरा': 'bad', 'खराब': 'poor', 'गलत': 'wrong',
                'परेशानी': 'trouble', 'दिक्कत': 'problem', 'गड़बड़': 'mess',
                'बेकार': 'useless', 'फालतू': 'waste', 'घटिया': 'cheap'
            },
            'transliteration_patterns': {
                'achha': 'good', 'badhiya': 'great', 'bekaar': 'useless',
                'ghatiya': 'cheap', 'zabardast': 'awesome', 'mast': 'nice',
                'bakwaas': 'nonsense', 'dhasu': 'cool'
            }
        }
        
    def _initialize_gemini(self):
        """Initialize Gemini with enhanced prompts for better classification"""
        if self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                # Try Gemini 2.5 Pro first, fallback to available models
                try:
                    self.gemini_model = genai.GenerativeModel(
                        model_name="gemini-2.5-pro",
                        generation_config={
                            "temperature": 0.2,  # Lower temperature for consistent analysis
                            "top_p": 0.9,
                            "max_output_tokens": 2048,
                        }
                    )
                except Exception:
                    # Fallback to Gemini 1.5 Pro
                    self.gemini_model = genai.GenerativeModel(
                        model_name="gemini-1.5-pro",
                        generation_config={
                            "temperature": 0.2,
                            "top_p": 0.9,
                            "max_output_tokens": 2048,
                        }
                    )
                print('✅ Enhanced Gemini sentiment analyzer initialized')
            except Exception as e:
                print(f'⚠️ Gemini initialization failed: {e}')
                self.gemini_model = None
        else:
            print('⚠️ No Gemini API key found')
            self.gemini_model = None
    
    async def analyze_comment_batch(self, comments: List[Dict], target_oem: str = None) -> List[Dict]:
        """Analyze a batch of comments with ADVANCED multi-layer classification"""
        print(f"🚀 Starting ADVANCED multi-layer sentiment analysis for {len(comments)} comments...")
        
        # Use the new advanced classifier for all analysis
        try:
            enhanced_comments = await self.advanced_classifier.analyze_comment_batch(comments, target_oem)
            
            # Generate batch summary
            summary = self.advanced_classifier.get_batch_summary(enhanced_comments)
            
            print(f"✅ ADVANCED Analysis Complete:")
            print(f"   📊 Total comments: {summary['total_comments']}")
            print(f"   💭 Sentiment: {summary['sentiment_distribution']}")
            print(f"   🌐 Multilingual: {summary['multilingual_percentage']}%")
            print(f"   🎭 Sarcasm detected: {summary['sarcasm_percentage']}%")
            print(f"   🎯 Avg confidence: {summary['average_confidence']}")
            print(f"   🏢 Company mentions: {summary['company_mentions']}")
            
            # Convert advanced classification to match expected format
            for comment in enhanced_comments:
                if 'advanced_sentiment_classification' in comment:
                    adv_classification = comment['advanced_sentiment_classification']
                    
                    # Map to expected format for backward compatibility
                    comment['sentiment_classification'] = {
                        'sentiment': adv_classification['sentiment'],
                        'confidence': adv_classification['confidence'],
                        'sarcasm_detected': adv_classification['sarcasm_detected'],
                        'sarcasm_score': adv_classification['sarcasm_score'],
                        'product_relevance': adv_classification['product_relevance'],
                        'relevance_score': adv_classification['relevance_score'],
                        'language_mix': adv_classification['language_analysis']['is_mixed'],
                        'context': adv_classification['context'],
                        'analysis_method': 'advanced_multi_layer_v2',
                        'key_factors': adv_classification.get('classification_factors', []),
                        'advanced_features': {
                            'emoji_analysis': adv_classification['emoji_analysis'],
                            'company_analysis': adv_classification['company_analysis'],
                            'engagement_analysis': adv_classification['engagement_analysis'],
                            'language_breakdown': adv_classification['language_analysis'],
                            'context_details': adv_classification['context_details']
                        }
                    }
            
            return enhanced_comments
            
        except Exception as e:
            print(f"⚠️ Advanced classifier failed: {e}, using fallback...")
            # Fallback to existing methods
            if self.gemini_model and len(comments) <= 20:
                return await self._ai_enhanced_analysis(comments, target_oem)
            else:
                return self._enhanced_rule_based_analysis(comments, target_oem)
    
    async def _ai_enhanced_analysis(self, comments: List[Dict], target_oem: str = None) -> List[Dict]:
        """AI-powered analysis using Gemini with enhanced prompts"""
        try:
            # Prepare comments for analysis
            comment_texts = []
            for i, comment in enumerate(comments):
                text = comment.get('text', '').strip()
                if text and len(text) > 5:
                    comment_texts.append({
                        'id': i,
                        'text': text,
                        'original_data': comment
                    })
            
            if not comment_texts:
                return comments
            
            # Create enhanced analysis prompt
            target_info = f" Focus on comments about {target_oem}." if target_oem else ""
            
            prompt = f"""You are an expert sentiment analysis AI specializing in Indian electric vehicle consumer feedback. You excel at detecting sarcasm, understanding context, handling multilingual content, and providing accurate classification.

TASK: Analyze these Indian electric vehicle user comments for advanced sentiment classification.{target_info}

For each comment, detect:
1. **SARCASM**: Is the comment sarcastic/ironic? (yes/no)
2. **PRODUCT_RELEVANCE**: Is it about electric vehicles/the target brand? (high/medium/low)
3. **SENTIMENT**: Overall sentiment (positive/negative/neutral)
4. **CONFIDENCE**: How confident are you? (0.0-1.0)
5. **LANGUAGE_MIX**: Contains Hindi/regional language? (yes/no)
6. **CONTEXT**: What aspect is discussed? (product/service/experience/general)

Comments to analyze:
{json.dumps([{'id': c['id'], 'text': c['text']} for c in comment_texts[:15]], indent=2, ensure_ascii=False)}

IMPORTANT GUIDELINES:
- Sarcasm indicators: Excessive punctuation, contradictory phrases, "too good to be true" statements, positive words in negative contexts
- Product relevance: Must mention EVs, brands, or related experiences explicitly
- Multilingual: Handle Hindi words (अच्छा=good, खराब=bad), transliterations, and code-switching
- Context matters: "Great service" with "visited 3 times" is likely sarcastic

Respond in JSON format:
{{
    "analyses": [
        {{
            "id": 0,
            "sarcasm_detected": true/false,
            "product_relevance": "high/medium/low",
            "sentiment": "positive/negative/neutral", 
            "confidence": 0.85,
            "language_mix": true/false,
            "context": "product/service/experience/general",
            "key_factors": ["brief explanation"]
        }}
    ],
    "batch_summary": {{
        "total_analyzed": X,
        "high_relevance_count": Y,
        "sarcasm_count": Z,
        "multilingual_count": W
    }}
}}"""

            # Generate analysis
            response = self.gemini_model.generate_content(prompt)
            result_text = response.text.strip()
            
            # Clean and parse JSON
            if result_text.startswith('```json'):
                result_text = result_text[7:-3]
            elif result_text.startswith('```'):
                result_text = result_text[3:-3]
            
            ai_result = json.loads(result_text)
            
            # Apply AI results to comments
            enhanced_comments = []
            for comment in comments:
                enhanced_comment = comment.copy()
                
                # Find corresponding analysis
                comment_analysis = None
                for analysis in ai_result.get('analyses', []):
                    if analysis['id'] < len(comment_texts):
                        original_comment = comment_texts[analysis['id']]['original_data']
                        if original_comment.get('text') == comment.get('text'):
                            comment_analysis = analysis
                            break
                
                if comment_analysis:
                    # Apply enhanced classification
                    enhanced_comment.update({
                        'sentiment_classification': {
                            'sentiment': comment_analysis['sentiment'],
                            'confidence': comment_analysis['confidence'],
                            'sarcasm_detected': comment_analysis['sarcasm_detected'],
                            'product_relevance': comment_analysis['product_relevance'],
                            'language_mix': comment_analysis['language_mix'],
                            'context': comment_analysis['context'],
                            'analysis_method': 'ai_enhanced',
                            'key_factors': comment_analysis.get('key_factors', [])
                        }
                    })
                else:
                    # Fallback to rule-based
                    enhanced_comment = self._apply_rule_based_classification(enhanced_comment, target_oem)
                
                enhanced_comments.append(enhanced_comment)
            
            print(f"✅ AI analysis completed for {len(enhanced_comments)} comments")
            return enhanced_comments
            
        except Exception as e:
            print(f"⚠️ AI analysis failed: {e}, using rule-based fallback")
            return self._enhanced_rule_based_analysis(comments, target_oem)
    
    def _enhanced_rule_based_analysis(self, comments: List[Dict], target_oem: str = None) -> List[Dict]:
        """Enhanced rule-based analysis with improved sarcasm and context detection"""
        enhanced_comments = []
        
        for comment in comments:
            enhanced_comment = self._apply_rule_based_classification(comment, target_oem)
            enhanced_comments.append(enhanced_comment)
        
        return enhanced_comments
    
    def _apply_rule_based_classification(self, comment: Dict, target_oem: str = None) -> Dict:
        """Apply rule-based classification with enhanced features"""
        text = comment.get('text', '').lower()
        enhanced_comment = comment.copy()
        
        # Sarcasm detection
        sarcasm_score = self._detect_sarcasm(text)
        
        # Product relevance detection
        relevance_score, relevance_level = self._detect_product_relevance(text, target_oem)
        
        # Multilingual detection and translation
        language_mix, translated_sentiment = self._detect_and_translate_multilingual(text)
        
        # Context detection
        context = self._detect_context(text)
        
        # Enhanced sentiment analysis
        sentiment, confidence = self._calculate_enhanced_sentiment(
            text, sarcasm_score, relevance_score, translated_sentiment
        )
        
        # Apply classification
        enhanced_comment['sentiment_classification'] = {
            'sentiment': sentiment,
            'confidence': confidence,
            'sarcasm_detected': sarcasm_score > 0.6,
            'sarcasm_score': round(sarcasm_score, 3),
            'product_relevance': relevance_level,
            'relevance_score': round(relevance_score, 3),
            'language_mix': language_mix,
            'context': context,
            'analysis_method': 'enhanced_rules',
            'translated_elements': translated_sentiment if language_mix else None
        }
        
        return enhanced_comment
    
    def _detect_sarcasm(self, text: str) -> float:
        """Detect sarcasm using pattern matching and linguistic cues"""
        sarcasm_score = 0.0
        
        # Check punctuation patterns
        for pattern in self.sarcasm_indicators['punctuation_patterns']:
            if re.search(pattern, text):
                sarcasm_score += 0.3
        
        # Check sarcastic phrases
        for pattern in self.sarcasm_indicators['phrase_patterns']:
            if re.search(pattern, text, re.IGNORECASE):
                sarcasm_score += 0.5
        
        # Check contradictory patterns
        for pattern in self.sarcasm_indicators['contradictory_patterns']:
            if re.search(pattern, text, re.IGNORECASE):
                sarcasm_score += 0.4
        
        # Additional sarcasm indicators
        # Exaggerated positivity in negative context (key improvement)
        positive_words_in_negative_context = ['best', 'perfect', 'amazing', 'great', 'excellent', 'wonderful']
        negative_context_words = ['service center', 'problem', 'issue', 'visit', 'times', 'again', 'repair', 'complaint']
        
        has_positive = any(word in text for word in positive_words_in_negative_context)
        has_negative_context = any(word in text for word in negative_context_words)
        
        if has_positive and has_negative_context:
            sarcasm_score += 0.7  # Strong indicator
        
        # "Great service" with multiple visits pattern (very common sarcasm)
        if re.search(r'(great|good|excellent|amazing).*(service|support)', text) and \
           re.search(r'(visit|times|again|3rd|third|multiple)', text):
            sarcasm_score += 0.8
        
        # Quotation marks around positive words (often sarcastic)
        if re.search(r'"(good|great|excellent|amazing)"', text):
            sarcasm_score += 0.5
        
        # Excessive enthusiasm with negative words
        if text.count('!') > 1 and any(neg in text for neg in ['bad', 'worst', 'terrible', 'awful']):
            sarcasm_score += 0.4
        
        # Pattern: positive word + ellipsis/dots (often indicates sarcasm)
        if re.search(r'(great|good|excellent|amazing|perfect).*\.{2,}', text):
            sarcasm_score += 0.5
        
        return min(1.0, sarcasm_score)
    
    def _detect_product_relevance(self, text: str, target_oem: str = None) -> Tuple[float, str]:
        """Detect if comment is relevant to electric vehicles and target OEM"""
        relevance_score = 0.0
        
        # Check for EV-related terms
        ev_matches = sum(1 for term in self.product_contexts['electric_vehicle_terms'] if term in text)
        relevance_score += min(1.0, ev_matches * 0.2)
        
        # Check for service-related terms
        service_matches = sum(1 for term in self.product_contexts['service_terms'] if term in text)
        relevance_score += min(0.5, service_matches * 0.15)
        
        # Check for experience terms
        exp_matches = sum(1 for term in self.product_contexts['experience_terms'] if term in text)
        relevance_score += min(0.3, exp_matches * 0.1)
        
        # Bonus for target OEM mention
        if target_oem and target_oem.lower() in text:
            relevance_score += 0.5
        
        # Penalty for generic/unrelated content
        generic_terms = ['movie', 'food', 'politics', 'weather', 'cricket', 'bollywood']
        if any(term in text for term in generic_terms) and relevance_score < 0.3:
            relevance_score *= 0.5
        
        # Determine relevance level
        if relevance_score >= 0.7:
            level = 'high'
        elif relevance_score >= 0.4:
            level = 'medium'
        else:
            level = 'low'
        
        return relevance_score, level
    
    def _detect_and_translate_multilingual(self, text: str) -> Tuple[bool, Dict]:
        """Detect multilingual content and translate sentiment indicators"""
        language_mix = False
        translated_sentiment = {}
        
        # Check for Hindi script (Devanagari)
        if re.search(r'[\u0900-\u097F]', text):
            language_mix = True
            
            # Translate Hindi sentiment words
            for hindi_word, english_meaning in self.multilingual_patterns['hindi_positive'].items():
                if hindi_word in text:
                    translated_sentiment[hindi_word] = {'meaning': english_meaning, 'sentiment': 'positive'}
            
            for hindi_word, english_meaning in self.multilingual_patterns['hindi_negative'].items():
                if hindi_word in text:
                    translated_sentiment[hindi_word] = {'meaning': english_meaning, 'sentiment': 'negative'}
        
        # Check for transliteration patterns
        for translit, meaning in self.multilingual_patterns['transliteration_patterns'].items():
            if translit in text:
                language_mix = True
                sentiment_val = 'positive' if meaning in ['good', 'great', 'awesome', 'nice', 'cool'] else 'negative'
                translated_sentiment[translit] = {'meaning': meaning, 'sentiment': sentiment_val}
        
        # Check for code-switching patterns (English + Hindi)
        hindi_words_present = bool(re.search(r'[\u0900-\u097F]', text))
        english_words_present = bool(re.search(r'[a-zA-Z]', text))
        if hindi_words_present and english_words_present:
            language_mix = True
        
        return language_mix, translated_sentiment
    
    def _detect_context(self, text: str) -> str:
        """Detect the context/aspect being discussed"""
        context_weights = defaultdict(float)
        
        # Product context
        product_terms = ['performance', 'speed', 'range', 'battery', 'design', 'features', 'quality']
        context_weights['product'] = sum(0.3 for term in product_terms if term in text)
        
        # Service context
        service_terms = ['service', 'support', 'center', 'maintenance', 'repair', 'staff', 'technician']
        context_weights['service'] = sum(0.4 for term in service_terms if term in text)
        
        # Experience context
        experience_terms = ['experience', 'journey', 'ownership', 'daily', 'commute', 'riding', 'driving']
        context_weights['experience'] = sum(0.35 for term in experience_terms if term in text)
        
        # Purchase/financial context
        financial_terms = ['price', 'cost', 'expensive', 'cheap', 'value', 'money', 'EMI', 'loan']
        context_weights['financial'] = sum(0.3 for term in financial_terms if term in text)
        
        # Return the context with highest weight
        if not context_weights:
            return 'general'
        
        return max(context_weights.items(), key=lambda x: x[1])[0]
    
    def _calculate_enhanced_sentiment(self, text: str, sarcasm_score: float, 
                                    relevance_score: float, translated_sentiment: Dict) -> Tuple[str, float]:
        """Calculate sentiment with sarcasm and relevance adjustments"""
        
        # Base sentiment calculation
        positive_words = [
            'good', 'great', 'excellent', 'amazing', 'awesome', 'perfect', 'love', 'best',
            'satisfied', 'happy', 'recommend', 'fantastic', 'wonderful', 'brilliant'
        ]
        
        negative_words = [
            'bad', 'terrible', 'awful', 'worst', 'hate', 'disappointed', 'poor', 'horrible',
            'useless', 'pathetic', 'disgusting', 'regret', 'waste', 'problem', 'issue'
        ]
        
        # Count sentiment words
        positive_count = sum(1 for word in positive_words if word in text)
        negative_count = sum(1 for word in negative_words if word in text)
        
        # Add translated sentiment
        for word_data in translated_sentiment.values():
            if word_data['sentiment'] == 'positive':
                positive_count += 1
            elif word_data['sentiment'] == 'negative':
                negative_count += 1
        
        # Calculate base sentiment score
        if positive_count > negative_count:
            base_sentiment = 'positive'
            confidence = min(0.9, 0.6 + (positive_count - negative_count) * 0.1)
        elif negative_count > positive_count:
            base_sentiment = 'negative'
            confidence = min(0.9, 0.6 + (negative_count - positive_count) * 0.1)
        else:
            base_sentiment = 'neutral'
            confidence = 0.5
        
        # Adjust for sarcasm
        if sarcasm_score > 0.6:
            if base_sentiment == 'positive':
                base_sentiment = 'negative'  # Sarcastic positive is actually negative
            confidence *= (1 - sarcasm_score * 0.3)  # Reduce confidence for sarcasm
        
        # Adjust confidence based on product relevance
        if relevance_score < 0.3:
            confidence *= 0.7  # Lower confidence for irrelevant comments
        
        # Ensure minimum confidence
        confidence = max(0.3, confidence)
        
        return base_sentiment, round(confidence, 3)
    
    def get_classification_summary(self, enhanced_comments: List[Dict]) -> Dict[str, Any]:
        """Generate summary of classification results"""
        total_comments = len(enhanced_comments)
        if total_comments == 0:
            return {'error': 'No comments to analyze'}
        
        # Count classifications
        sentiment_counts = defaultdict(int)
        relevance_counts = defaultdict(int)
        context_counts = defaultdict(int)
        sarcasm_count = 0
        multilingual_count = 0
        high_confidence_count = 0
        
        total_confidence = 0
        
        for comment in enhanced_comments:
            classification = comment.get('sentiment_classification', {})
            
            sentiment_counts[classification.get('sentiment', 'unknown')] += 1
            relevance_counts[classification.get('product_relevance', 'unknown')] += 1
            context_counts[classification.get('context', 'unknown')] += 1
            
            if classification.get('sarcasm_detected', False):
                sarcasm_count += 1
            
            if classification.get('language_mix', False):
                multilingual_count += 1
            
            confidence = classification.get('confidence', 0)
            total_confidence += confidence
            
            if confidence > 0.7:
                high_confidence_count += 1
        
        avg_confidence = total_confidence / total_comments
        
        return {
            'total_comments': total_comments,
            'sentiment_distribution': dict(sentiment_counts),
            'relevance_distribution': dict(relevance_counts),
            'context_distribution': dict(context_counts),
            'sarcasm_detected_count': sarcasm_count,
            'sarcasm_percentage': round((sarcasm_count / total_comments) * 100, 2),
            'multilingual_count': multilingual_count,
            'multilingual_percentage': round((multilingual_count / total_comments) * 100, 2),
            'average_confidence': round(avg_confidence, 3),
            'high_confidence_count': high_confidence_count,
            'high_confidence_percentage': round((high_confidence_count / total_comments) * 100, 2),
            'classification_quality': {
                'excellent': high_confidence_count,
                'good': sum(1 for c in enhanced_comments 
                           if 0.5 < c.get('sentiment_classification', {}).get('confidence', 0) <= 0.7),
                'needs_review': sum(1 for c in enhanced_comments 
                                  if c.get('sentiment_classification', {}).get('confidence', 0) <= 0.5)
            }
        }
