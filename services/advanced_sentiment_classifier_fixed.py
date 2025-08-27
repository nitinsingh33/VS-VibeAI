"""
Advanced Sentiment Classifier with Enhanced Features
- Language Detection (English vs Local Languages)
- Emoji Sentiment Analysis
- Company/Product Mention Attribution
- Engagement-based Weighting
- Multi-layered Classification Approach
"""

import re
import json
import asyncio
from typing import Dict, List, Any, Tuple, Optional
from collections import defaultdict
import unicodedata

class AdvancedSentimentClassifier:
    def __init__(self):
        self.initialize_language_patterns()
        self.initialize_emoji_mapping()
        self.initialize_company_patterns()
        self.initialize_sentiment_patterns()
        
    def initialize_language_patterns(self):
        """Initialize patterns for language detection"""
        # English patterns
        self.english_patterns = {
            'words': [
                'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by',
                'good', 'bad', 'best', 'worst', 'love', 'hate', 'like', 'dislike',
                'service', 'battery', 'range', 'price', 'quality', 'performance'
            ],
            'contractions': ["don't", "won't", "can't", "shouldn't", "wouldn't", "couldn't", "isn't", "aren't"],
            'pronouns': ['i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them']
        }
        
        # Hindi/Local language patterns
        self.local_language_patterns = {
            'hindi_words': [
                'है', 'के', 'में', 'से', 'को', 'का', 'की', 'और', 'या', 'लेकिन',
                'अच्छा', 'बुरा', 'अच्छी', 'बुरी', 'बेहतरीन', 'खराब', 'प्यार', 'नफरत',
                'सर्विस', 'बैटरी', 'रेंज', 'कीमत', 'गुणवत्ता', 'प्रदर्शन'
            ],
            'tamil_words': [
                'इது', 'அது', 'என்', 'உன்', 'अवन्', 'अवळ्', 'नम्', 'अवर्गळ्',
                'नल्ल', 'गेट्ट', 'सिरन्त', 'मोसमान', 'गातल्', 'वेरुप्पु'
            ],
            'malayalam_words': [
                'ഇത്', 'അത്', 'എന്റെ', 'നിന്റെ', 'അവന്റെ', 'അവളുടെ', 'നമ്മുടെ',
                'നല്ല', 'മോശം', 'മികച്ച', 'കുറ്റം', 'സ്നേഹം', 'വെറുപ്പ്'
            ],
            'telugu_words': [
                'ఇది', 'అది', 'నా', 'నీ', 'అతని', 'ఆమె', 'మా', 'వారి',
                'మంచి', 'చెడు', 'అత్యుత్తమ', 'చెత్త', 'ప్రేమ', 'ద్వేషం'
            ]
        }
        
        # Script detection patterns
        self.script_patterns = {
            'devanagari': re.compile(r'[\u0900-\u097F]+'),  # Hindi
            'tamil': re.compile(r'[\u0B80-\u0BFF]+'),       # Tamil
            'malayalam': re.compile(r'[\u0D00-\u0D7F]+'),   # Malayalam
            'telugu': re.compile(r'[\u0C00-\u0C7F]+'),      # Telugu
            'bengali': re.compile(r'[\u0980-\u09FF]+'),     # Bengali
            'gujarati': re.compile(r'[\u0A80-\u0AFF]+'),    # Gujarati
            'kannada': re.compile(r'[\u0C80-\u0CFF]+'),     # Kannada
        }

    def initialize_emoji_mapping(self):
        """Initialize emoji sentiment mapping"""
        self.emoji_sentiment = {
            # Positive emojis
            '😊': 0.8, '😀': 0.9, '😃': 0.9, '😄': 0.9, '😁': 0.8, '😆': 0.7,
            '😍': 0.9, '🥰': 0.9, '😘': 0.8, '😗': 0.7, '😙': 0.7, '😚': 0.8,
            '🤗': 0.8, '🤩': 0.9, '😇': 0.8, '🙂': 0.6, '😉': 0.7,
            '👍': 0.8, '👌': 0.7, '👏': 0.8, '🙌': 0.8, '💯': 0.9, '✨': 0.7,
            '⭐': 0.8, '🌟': 0.8, '💫': 0.7, '🔥': 0.8, '💪': 0.8, '🚀': 0.9,
            '❤️': 0.9, '💖': 0.9, '💕': 0.8, '💗': 0.8, '💓': 0.8, '💝': 0.8,
            '😂': 0.8, '🤣': 0.8, '😹': 0.7, '😻': 0.8, '🥳': 0.9, '🎉': 0.8,
            '❤': 0.9, '🧡': 0.8, '💛': 0.8, '💚': 0.8, '💙': 0.8, '💜': 0.8,
            
            # Negative emojis
            '😠': -0.8, '😡': -0.9, '🤬': -0.9, '😤': -0.7, '😒': -0.6, '🙄': -0.5,
            '😞': -0.7, '😔': -0.7, '😟': -0.6, '😕': -0.6, '🙁': -0.6, '☹️': -0.7,
            '😣': -0.7, '😖': -0.7, '😫': -0.8, '😩': -0.8, '🥺': -0.6, '😢': -0.8,
            '😭': -0.9, '😰': -0.7, '😨': -0.7, '😱': -0.8, '🤯': -0.7, '😳': -0.5,
            '👎': -0.8, '🤦': -0.7, '🤷': -0.3, '💔': -0.9, '😵': -0.8, '🤮': -0.9,
            
            # Neutral emojis
            '😐': 0.0, '😑': 0.0, '🤔': 0.0, '🧐': 0.0, '🤨': 0.0, '😶': 0.0,
            '🙏': 0.6, '🕉️': 0.5, '🪔': 0.6, '🎊': 0.7, '🎈': 0.6, '🎁': 0.7,
        }

    def initialize_company_patterns(self):
        """Initialize company/OEM detection patterns"""
        self.company_patterns = {
            'ola_electric': [
                'ola electric', 'ola', 's1', 's1 pro', 's1 air', 'ola scooter',
                'ola bike', 'ola ev', 'ola s1', 'olaelectric'
            ],
            'ather': [
                'ather', '450x', '450 plus', '450plus', 'ather energy',
                'ather scooter', 'ather bike', 'ather ev'
            ],
            'bajaj_chetak': [
                'bajaj chetak', 'chetak', 'bajaj', 'bajaj electric',
                'chetak electric', 'bajaj ev'
            ],
            'tvs_iqube': [
                'tvs iqube', 'iqube', 'tvs', 'tvs electric', 'tvs ev',
                'iqube electric', 'i-qube', 'tvs motor'
            ],
            'hero_vida': [
                'hero vida', 'vida', 'hero electric', 'hero ev',
                'vida v1', 'hero motocorp'
            ]
        }

    def initialize_sentiment_patterns(self):
        """Initialize comprehensive sentiment patterns"""
        self.positive_patterns = {
            'english': [
                'excellent', 'amazing', 'fantastic', 'wonderful', 'great', 'awesome',
                'perfect', 'outstanding', 'superb', 'brilliant', 'love', 'like',
                'good', 'better', 'best', 'impressive', 'satisfied', 'happy',
                'recommend', 'worth', 'value', 'quality', 'smooth', 'comfortable'
            ],
            'hindi': [
                'अच्छा', 'बेहतरीन', 'शानदार', 'बढ़िया', 'मस्त', 'कमाल',
                'सबसे अच्छा', 'खुश', 'संतुष्ट', 'पसंद', 'प्यार'
            ]
        }
        
        self.negative_patterns = {
            'english': [
                'terrible', 'awful', 'horrible', 'worst', 'bad', 'poor',
                'disappointed', 'unsatisfied', 'hate', 'dislike', 'regret',
                'waste', 'useless', 'pathetic', 'fraud', 'cheat', 'scam'
            ],
            'hindi': [
                'बुरा', 'खराब', 'बकवास', 'गंदा', 'घटिया', 'धोखा',
                'फ्रॉड', 'बेकार', 'निकम्मा', 'नफरत', 'गुस्सा'
            ]
        }

    def analyze_emojis(self, text: str) -> Dict[str, Any]:
        """Analyze emoji sentiment in text"""
        emojis_found = []
        emoji_scores = []
        
        for char in text:
            if char in self.emoji_sentiment:
                emojis_found.append(char)
                emoji_scores.append(self.emoji_sentiment[char])
        
        if not emoji_scores:
            return {
                'has_emojis': False,
                'emoji_count': 0,
                'emoji_sentiment': 'neutral',
                'emoji_sentiment_score': 0.0,
                'emojis_found': []
            }
        
        avg_emoji_sentiment = sum(emoji_scores) / len(emoji_scores)
        
        if avg_emoji_sentiment > 0.3:
            emoji_sentiment = 'positive'
        elif avg_emoji_sentiment < -0.3:
            emoji_sentiment = 'negative'
        else:
            emoji_sentiment = 'neutral'
        
        return {
            'has_emojis': True,
            'emoji_count': len(emojis_found),
            'emoji_sentiment': emoji_sentiment,
            'emoji_sentiment_score': round(avg_emoji_sentiment, 3),
            'emojis_found': emojis_found
        }

    def detect_language_mix(self, text: str) -> Dict[str, Any]:
        """Detect if text is mixed language and identify primary language"""
        text_lower = text.lower()
        
        # Count English words
        english_count = 0
        for word in self.english_patterns['words']:
            if word in text_lower:
                english_count += 1
        
        # Count local language words
        local_count = 0
        detected_languages = []
        
        for lang, words in self.local_language_patterns.items():
            lang_count = 0
            for word in words:
                if word in text_lower:
                    lang_count += 1
                    local_count += 1
            if lang_count > 0:
                detected_languages.append(lang)
        
        # Script detection
        script_detected = []
        for script, pattern in self.script_patterns.items():
            if pattern.search(text):
                script_detected.append(script)
        
        # Determine primary language
        if english_count > local_count:
            primary_language = 'english'
        elif local_count > 0:
            primary_language = 'local_words'
        elif script_detected:
            primary_language = script_detected[0]
        else:
            primary_language = 'unknown'
        
        is_mixed = english_count > 0 and local_count > 0
        
        return {
            'is_mixed': is_mixed,
            'primary_language': primary_language,
            'english_words': english_count,
            'local_words': local_count,
            'languages': detected_languages,
            'scripts': script_detected
        }

    def detect_company_mentions(self, text: str) -> Dict[str, Any]:
        """Detect company/OEM mentions in text"""
        text_lower = text.lower()
        mentions = {}
        all_mentions = {}
        
        for company, patterns in self.company_patterns.items():
            company_score = 0
            matched_patterns = []
            
            for pattern in patterns:
                if pattern in text_lower:
                    company_score += 1
                    matched_patterns.append(pattern)
            
            if company_score > 0:
                mentions[company] = {
                    'score': company_score,
                    'patterns': matched_patterns,
                    'confidence': min(company_score / len(patterns), 1.0)
                }
                all_mentions[company] = mentions[company]
        
        primary_company = None
        if mentions:
            primary_company = max(mentions.keys(), key=lambda x: mentions[x]['score'])
        
        return {
            'has_mentions': len(mentions) > 0,
            'primary_company': primary_company,
            'all_mentions': all_mentions,
            'mention_count': len(mentions)
        }

    def calculate_engagement_weight(self, likes: int, replies: int, shares: int) -> Dict[str, Any]:
        """Calculate engagement-based sentiment weight"""
        # Normalize engagement metrics
        like_weight = min(likes / 100.0, 0.5) if likes > 0 else 0.0
        reply_weight = min(replies / 20.0, 0.4) if replies > 0 else 0.0
        share_weight = min(shares / 10.0, 0.3) if shares > 0 else 0.0
        
        # Combined engagement score
        engagement_score = like_weight + reply_weight + share_weight
        
        # Engagement categories
        if engagement_score >= 1.5:
            engagement_level = 'viral'
        elif engagement_score >= 1.0:
            engagement_level = 'high'
        elif engagement_score >= 0.5:
            engagement_level = 'medium'
        elif engagement_score > 0:
            engagement_level = 'low'
        else:
            engagement_level = 'none'
        
        # Sentiment amplification factor
        if engagement_level == 'viral':
            amplification_factor = 1.5
        elif engagement_level == 'high':
            amplification_factor = 1.3
        elif engagement_level == 'medium':
            amplification_factor = 1.1
        else:
            amplification_factor = 1.0
        
        return {
            'engagement_score': round(engagement_score, 3),
            'engagement_level': engagement_level,
            'amplification_factor': amplification_factor,
            'like_weight': round(like_weight, 3),
            'reply_weight': round(reply_weight, 3),
            'share_weight': round(share_weight, 3)
        }

    def analyze_sentiment_patterns(self, text: str, language_info: Dict) -> Dict[str, Any]:
        """Analyze sentiment using pattern matching with enhanced Hindi-English transliteration support"""
        text_lower = text.lower()
        positive_score = 0
        negative_score = 0
        sentiment_words = []
        
        # Enhanced transliteration corrections - especially for the case you mentioned
        transliteration_corrections = {
            # Strong positive expressions
            'gajab he': 'positive',
            'gajab hai': 'positive',
            'गजब है': 'positive',
            'gajab': 'positive',
            'so good': 'positive',
            'bilkul problem nahi': 'positive',
            'bilkul problem nahi he': 'positive',
            'bilkul problem nahi hai': 'positive',
            'बिल्कुल प्रॉब्लम नहीं': 'positive',
            'बिल्कुल प्रॉब्लम नहीं है': 'positive',
            'update ke baad': 'neutral',  # After update - context dependent
            'अपडेट के बाद': 'neutral',
            'mene bhi': 'neutral',  # I also
            'मैंने भी': 'neutral',
            'bhai': 'neutral',  # Brother - casual address
            'भाई': 'neutral',
            's1 air leli': 'neutral',  # Bought S1 Air
            'leli': 'neutral',  # Bought/taken
            'लेली': 'neutral',
            'aur': 'neutral',  # And
            'और': 'neutral',
            
            # Positive patterns from your example
            'bhot achhi': 'positive',
            'बहुत अच्छी': 'positive',
            'bahut achhi': 'positive',
            'bahut acchi': 'positive',
            'bhot acchi': 'positive',
            'bhot achha': 'positive',
            'बहुत अच्छा': 'positive',
            'bahut achha': 'positive',
            'bahut accha': 'positive',
            'bhot accha': 'positive',
            
            # Other positive patterns
            'bhot badhiya': 'positive',
            'बहुत बढ़िया': 'positive',
            'bahut badhiya': 'positive',
            'bhot badiya': 'positive',
            'बहुत बडिया': 'positive',
            'bahut badiya': 'positive',
            'ekdum mast': 'positive',
            'एकदम मस्त': 'positive',
            'bilkul sahi': 'positive',
            'बिल्कुल सही': 'positive',
            'bhot sahi': 'positive',
            'बहुत सही': 'positive',
            'bahut sahi': 'positive',
            
            # Negative patterns
            'problem bahut': 'negative',
            'समस्या बहुत': 'negative',
            'samasya bahut': 'negative',
            'bhot problem': 'negative',
            'बहुत प्रॉब्लम': 'negative',
            'bahut problem': 'negative',
        }
        
        # Apply transliteration corrections first
        for word, sentiment in transliteration_corrections.items():
            if word in text_lower:
                if sentiment == 'positive':
                    positive_score += 2.0  # Strong weight for transliteration matches
                    sentiment_words.append({'word': word, 'sentiment': 'positive', 'language': 'transliteration'})
                elif sentiment == 'negative':
                    negative_score += 2.0
                    sentiment_words.append({'word': word, 'sentiment': 'negative', 'language': 'transliteration'})
                else:  # neutral
                    sentiment_words.append({'word': word, 'sentiment': 'neutral', 'language': 'transliteration'})
        
        # Apply language-specific patterns
        if (language_info['primary_language'] in ['english', 'unknown'] or 
            'english' in language_info['languages'] or 
            language_info['is_mixed']):
            
            for word in self.positive_patterns['english']:
                if re.search(r'\b' + re.escape(word) + r'\b', text_lower):
                    # Avoid double counting if already caught by transliteration
                    if not any(trans_word in text_lower and word in trans_word for trans_word in transliteration_corrections.keys()):
                        positive_score += 1
                        sentiment_words.append({'word': word, 'sentiment': 'positive', 'language': 'english'})
            
            for word in self.negative_patterns['english']:
                if re.search(r'\b' + re.escape(word) + r'\b', text_lower):
                    if not any(trans_word in text_lower and word in trans_word for trans_word in transliteration_corrections.keys()):
                        negative_score += 1
                        sentiment_words.append({'word': word, 'sentiment': 'negative', 'language': 'english'})
        
        if language_info['primary_language'] in ['devanagari', 'local_words'] or language_info['is_mixed']:
            for word in self.positive_patterns['hindi']:
                if word in text_lower:
                    positive_score += 1
                    sentiment_words.append({'word': word, 'sentiment': 'positive', 'language': 'hindi'})
            
            for word in self.negative_patterns['hindi']:
                if word in text_lower:
                    negative_score += 1
                    sentiment_words.append({'word': word, 'sentiment': 'negative', 'language': 'hindi'})
        
        # Calculate final sentiment
        total_score = positive_score + negative_score
        
        if total_score == 0:
            sentiment = 'neutral'
            confidence = 0.3
        elif positive_score > negative_score:
            sentiment = 'positive'
            confidence = min(0.9, 0.5 + (positive_score - negative_score) / total_score * 0.4)
        else:
            sentiment = 'negative'
            confidence = min(0.9, 0.5 + (negative_score - positive_score) / total_score * 0.4)
        
        return {
            'sentiment': sentiment,
            'confidence': round(confidence, 3),
            'positive_score': round(positive_score, 2),
            'negative_score': round(negative_score, 2),
            'sentiment_words': sentiment_words,
            'text': text
        }

    async def classify_comment_advanced(self, comment: Dict, target_oem: str = None) -> Dict[str, Any]:
        """Perform advanced multi-layered sentiment classification"""
        text = comment.get('text', '')
        likes = comment.get('likes', 0)
        replies = comment.get('replies', 0)
        shares = comment.get('shares', 0)
        
        if not text:
            return self._create_default_classification()
        
        # Analyze different aspects
        language_info = self.detect_language_mix(text)
        emoji_info = self.analyze_emojis(text)
        company_info = self.detect_company_mentions(text)
        engagement_info = self.calculate_engagement_weight(likes, replies, shares)
        pattern_sentiment = self.analyze_sentiment_patterns(text, language_info)
        
        # Calculate final sentiment
        final_sentiment = self._calculate_final_sentiment(
            pattern_sentiment, emoji_info, engagement_info, company_info, target_oem
        )
        
        return {
            'sentiment': final_sentiment['sentiment'],
            'confidence': final_sentiment['confidence'],
            'language_analysis': language_info,
            'emoji_analysis': emoji_info,
            'company_analysis': company_info,
            'engagement_analysis': engagement_info,
            'pattern_analysis': pattern_sentiment,
            'analysis_method': 'advanced_multi_layer',
            'classification_factors': final_sentiment['factors']
        }

    def _calculate_final_sentiment(self, pattern_sentiment: Dict, emoji_info: Dict, 
                                  engagement_info: Dict, company_info: Dict, 
                                  target_oem: str) -> Dict[str, Any]:
        """Calculate final sentiment by combining all factors"""
        
        factors = []
        base_sentiment = pattern_sentiment['sentiment']
        base_confidence = pattern_sentiment['confidence']
        factors.append(f"pattern_sentiment: {base_sentiment} (conf: {base_confidence})")
        
        # Emoji influence
        emoji_influence = 0.0
        if emoji_info['has_emojis']:
            emoji_influence = emoji_info['emoji_sentiment_score'] * 0.3
            factors.append(f"emoji_influence: {emoji_influence:.2f}")
        
        # Engagement boost
        if engagement_info['engagement_level'] in ['high', 'viral']:
            base_confidence *= engagement_info['amplification_factor']
            factors.append(f"engagement_boost: {engagement_info['amplification_factor']}")
        
        # Calculate final score
        final_score = 0
        if base_sentiment == 'positive':
            final_score = 1
        elif base_sentiment == 'negative':
            final_score = -1
        
        final_score += emoji_influence
        
        # Determine final sentiment
        if final_score > 0.3:
            final_sentiment = 'positive'
        elif final_score < -0.3:
            final_sentiment = 'negative'
        else:
            final_sentiment = 'neutral'
        
        final_confidence = max(0.3, min(0.95, base_confidence))
        
        return {
            'sentiment': final_sentiment,
            'confidence': round(final_confidence, 3),
            'factors': factors,
            'final_score': round(final_score, 3)
        }

    def _create_default_classification(self) -> Dict[str, Any]:
        """Create default classification for empty or invalid text"""
        return {
            'sentiment': 'neutral',
            'confidence': 0.3,
            'language_analysis': {'is_mixed': False, 'primary_language': 'unknown'},
            'emoji_analysis': {'has_emojis': False, 'emoji_sentiment': 'neutral'},
            'company_analysis': {'has_mentions': False, 'primary_company': None},
            'engagement_analysis': {'engagement_level': 'none'},
            'analysis_method': 'default'
        }

    async def analyze_comment_batch(self, comments: List[Dict], target_oem: str = None) -> List[Dict]:
        """Analyze a batch of comments with advanced classification"""
        enhanced_comments = []
        
        for comment in comments:
            try:
                classification = await self.classify_comment_advanced(comment, target_oem)
                enhanced_comment = comment.copy()
                enhanced_comment['advanced_sentiment_classification'] = classification
                enhanced_comments.append(enhanced_comment)
            except Exception as e:
                enhanced_comment = comment.copy()
                enhanced_comment['advanced_sentiment_classification'] = self._create_default_classification()
                enhanced_comments.append(enhanced_comment)
        
        return enhanced_comments

# Test the specific case you mentioned
async def test_specific_case():
    """Test the specific case mentioned by the user"""
    classifier = AdvancedSentimentClassifier()
    
    test_comment = {
        'text': 'Ola bhai gajab he mene bhi s1 air leli aur update ke baad bilkul problem nahi he ❤so good scooter',
        'likes': 5,
        'replies': 2,
        'shares': 1
    }
    
    result = await classifier.classify_comment_advanced(test_comment, 'ola_electric')
    
    print("="*60)
    print("SENTIMENT ANALYSIS RESULT")
    print("="*60)
    print(f"Text: {test_comment['text']}")
    print(f"Sentiment: {result['sentiment']}")
    print(f"Confidence: {result['confidence']}")
    print(f"Pattern Analysis: {result['pattern_analysis']['sentiment']} (score: +{result['pattern_analysis']['positive_score']}, -{result['pattern_analysis']['negative_score']})")
    print(f"Emoji Analysis: {result['emoji_analysis']['emoji_sentiment']} (score: {result['emoji_analysis']['emoji_sentiment_score']})")
    print(f"Language Mix: {result['language_analysis']['is_mixed']}")
    print(f"Company Mentioned: {result['company_analysis']['primary_company']}")
    print(f"Sentiment Words Found:")
    for word_info in result['pattern_analysis']['sentiment_words']:
        print(f"  - '{word_info['word']}' ({word_info['sentiment']}, {word_info['language']})")
    print("="*60)

if __name__ == "__main__":
    # Run the test
    asyncio.run(test_specific_case())
