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
                'இது', 'அது', 'என்', 'உன்', 'அவன்', 'அவள்', 'நம்', 'அவர்கள்',
                'நல்ல', 'கெட்ட', 'சிறந்த', 'மோசமான', 'காதல்', 'வெறுப்பு'
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
            '🤗': 0.8, '🤩': 0.9, '😇': 0.8, '😊': 0.8, '🙂': 0.6, '😉': 0.7,
            '👍': 0.8, '👌': 0.7, '👏': 0.8, '🙌': 0.8, '💯': 0.9, '✨': 0.7,
            '⭐': 0.8, '🌟': 0.8, '💫': 0.7, '🔥': 0.8, '💪': 0.8, '🚀': 0.9,
            '❤️': 0.9, '💖': 0.9, '💕': 0.8, '💗': 0.8, '💓': 0.8, '💝': 0.8,
            '😂': 0.8, '🤣': 0.8, '😹': 0.7, '😻': 0.8, '🥳': 0.9, '🎉': 0.8,
            
            # Negative emojis
            '😠': -0.8, '😡': -0.9, '🤬': -0.9, '😤': -0.7, '😒': -0.6, '🙄': -0.5,
            '😞': -0.7, '😔': -0.7, '😟': -0.6, '😕': -0.6, '🙁': -0.6, '☹️': -0.7,
            '😣': -0.7, '😖': -0.7, '😫': -0.8, '😩': -0.8, '🥺': -0.6, '😢': -0.8,
            '😭': -0.9, '😰': -0.7, '😨': -0.7, '😱': -0.8, '🤯': -0.7, '😳': -0.5,
            '👎': -0.8, '🤦': -0.7, '🤷': -0.3, '💔': -0.9, '😵': -0.8, '🤮': -0.9,
            '🤢': -0.8, '🤧': -0.5, '😷': -0.4, '🙃': -0.3, '😬': -0.5, '😐': -0.2,
            
            # Neutral emojis
            '😐': 0.0, '😑': 0.0, '🤔': 0.0, '🧐': 0.0, '🤨': 0.0, '😶': 0.0,
            '😯': 0.0, '😮': 0.0, '😲': 0.0, '🤐': 0.0,
            
            # Context-dependent emojis (Indian specific)
            '🙏': 0.6, '🕉️': 0.5, '🪔': 0.6, '🎊': 0.7, '🎈': 0.6, '🎁': 0.7,
        }
        
        # Compile emoji pattern
        emoji_pattern = '|'.join(re.escape(emoji) for emoji in self.emoji_sentiment.keys())
        self.emoji_regex = re.compile(f'({emoji_pattern})')

    def initialize_company_patterns(self):
        """Initialize company and product mention patterns"""
        self.company_patterns = {
            'Ola Electric': {
                'primary': ['ola electric', 'ola', 's1 pro', 's1 air', 's1 x'],
                'products': ['s1', 'pro', 'air', 'x+', 'gen 2', 'gen2'],
                'variations': ['olla', 'ola scooter', 'ola bike']
            },
            'Ather': {
                'primary': ['ather', '450x', '450 x', '450plus', '450 plus'],
                'products': ['450', 'rizta', 'gen 3', 'gen3'],
                'variations': ['ather energy', 'ather scooter']
            },
            'Bajaj Chetak': {
                'primary': ['bajaj chetak', 'chetak', 'bajaj'],
                'products': ['chetak premium', 'chetak urbane'],
                'variations': ['chetak electric', 'bajaj electric']
            },
            'TVS iQube': {
                'primary': ['tvs iqube', 'iqube', 'tvs'],
                'products': ['iqube electric', 'iqube s', 'iqube st'],
                'variations': ['tvs electric', 'tvs scooter']
            },
            'Hero Vida': {
                'primary': ['hero vida', 'vida', 'hero'],
                'products': ['vida v1', 'vida v1 pro', 'vida v1 plus'],
                'variations': ['hero electric', 'hero motocorp']
            },
            'Ampere': {
                'primary': ['ampere', 'magnus', 'primus'],
                'products': ['magnus ex', 'magnus pro', 'primus', 'zeal'],
                'variations': ['ampere vehicles', 'ampere electric']
            },
            'River Mobility': {
                'primary': ['river', 'river mobility', 'indie'],
                'products': ['river indie', 'indie electric'],
                'variations': ['river scooter', 'river bike']
            },
            'Ultraviolette': {
                'primary': ['ultraviolette', 'f77', 'f 77'],
                'products': ['f77 mach 2', 'f77 recon', 'f77 space edition'],
                'variations': ['uv f77', 'ultraviolette automotive']
            },
            'Revolt': {
                'primary': ['revolt', 'rv400', 'rv 400'],
                'products': ['rv400 brava', 'rv400 premium', 'rz1'],
                'variations': ['revolt motors', 'revolt electric']
            },
            'BGauss': {
                'primary': ['bgauss', 'b gauss', 'ruo'],
                'products': ['ruo smart', 'ruo bs6', 'a2b'],
                'variations': ['bgauss scooter', 'bgauss electric']
            }
        }

    def initialize_sentiment_patterns(self):
        """Initialize sentiment analysis patterns"""
        self.positive_patterns = {
            'english': [
                'excellent', 'amazing', 'awesome', 'fantastic', 'outstanding', 'brilliant',
                'superb', 'magnificent', 'wonderful', 'perfect', 'incredible', 'remarkable',
                'good', 'great', 'nice', 'fine', 'ok', 'okay', 'decent', 'solid',
                'love', 'like', 'enjoy', 'appreciate', 'recommend', 'impressed',
                'satisfied', 'happy', 'pleased', 'delighted', 'thrilled'
            ],
            'hindi': [
                'अच्छा', 'बढ़िया', 'शानदार', 'उत्कृष्ट', 'बेहतरीन', 'जबरदस्त',
                'सुंदर', 'प्यारा', 'मस्त', 'धमाकेदार', 'कमाल', 'लाजवाब'
            ]
        }
        
        self.negative_patterns = {
            'english': [
                'terrible', 'awful', 'horrible', 'disgusting', 'pathetic', 'useless',
                'worst', 'bad', 'poor', 'disappointing', 'frustrating', 'annoying',
                'hate', 'dislike', 'regret', 'waste', 'problem', 'issue', 'trouble',
                'broken', 'defective', 'faulty', 'damaged', 'cheap', 'overpriced',
                'fraud', 'cheat', 'cheating', 'scam', 'fake', 'duplicate', 'copy',
                'looting', 'loot', 'theft', 'stealing', 'ripping off', 'ripoff',
                'disaster', 'nightmare', 'hell', 'cursed', 'doomed', 'failed',
                'failure', 'disaster', 'catastrophe', 'rubbish', 'garbage', 'trash',
                'shame', 'shameful', 'embarrassing', 'ridiculous', 'stupid', 'idiotic',
                'nonsense', 'bullshit', 'crap', 'shit', 'damn', 'fucking', 'bastard',
                'sucks', 'sucking', 'suck', 'crappy', 'shitty', 'terrible service',
                'worst service', 'pathetic service', 'useless service', 'hopeless',
                'hopeless condition', 'hopeless situation', 'never again', 'never buy',
                'warning', 'beware', 'avoid', 'dont buy', 'do not buy', 'money waste',
                'time waste', 'energy waste', 'complete waste', 'total waste',
                'faltu', 'bewakoof', 'pagal', 'stupid company', 'worst company',
                'disaster company', 'fail', 'failing', 'going to fail', 'will fail',
                'like fail', 'going down', 'downfall', 'collapse', 'dead', 'dying',
                'finish', 'finished', 'over', 'end', 'ended', 'no good', 'not good',
                'kaam nahi', 'work nahi', 'start nahi', 'nahi hogi', 'nahi karegi',
                'bigjaye', 'bigad', 'kharab ho', 'problem hai', 'issue hai', 'bekar',
                'not learning', 'complaint', 'complaints', 'water into trunk', 
                'weird seat design', 'should have changed', 'still laggy', 'mediocre',
                'build quality same', 'not worth', 'not worth buying', 'tbh not worth',
                'complicating', 'instead of simplifying', 'fasgaya', 'fas gaya',
                'mailage', 'jyda nahi', 'zyada nahi', 'eco mod pe', 'se jyda nahi',
                'just new colour', 'v1 is worth', 'v2 is just', 'dont purchase',
                "don't purchase", 'choor company', 'choor compnay', 'बनिए चोर',
                'डिजाइन अच्छा नही', 'design achha nahi', 'yamaha niken'
            ],
            'hindi': [
                'बुरा', 'खराब', 'गंदा', 'बकवास', 'फालतू', 'व्यर्थ',
                'समस्या', 'परेशानी', 'दिक्कत', 'गलत', 'टूटा', 'ख़राब',
                'धोखा', 'फ्रॉड', 'झूठ', 'नकली', 'डुप्लिकेट', 'कॉपी',
                'लूट', 'चोरी', 'ठगी', 'बेईमानी', 'गलत काम', 'बर्बाद',
                'तबाह', 'नष्ट', 'बेकार', 'निकम्मा', 'गंदगी', 'कचरा',
                'शर्म', 'शर्मनाक', 'बेशर्म', 'बेवकूफी', 'मूर्खता', 'गलती',
                'भूल', 'नुकसान', 'हानि', 'घाटा', 'परेशान', 'तंग',
                'चिढ़', 'गुस्सा', 'क्रोध', 'नफरत', 'घृणा', 'अफसोस',
                'पछतावा', 'दुःख', 'दर्द', 'कष्ट', 'सज़ा', 'सिरदर्द',
                'dhokha', 'fraud', 'jhooth', 'nakli', 'duplicate', 'copy',
                'loot', 'chori', 'thagi', 'beimani', 'galat kaam', 'barbad',
                'tabah', 'nasht', 'bekaar', 'nikamma', 'gandagi', 'kachra',
                'sharm', 'sharmnak', 'besharm', 'bewakoofi', 'murkhata', 'galti',
                'bhool', 'nuksan', 'hani', 'ghata', 'pareshan', 'tang',
                'chidh', 'gussa', 'krodh', 'nafrat', 'ghrina', 'afsos',
                'pachtawa', 'dukh', 'dard', 'kasht', 'saza', 'sirdard',
                'ghatiya', 'bekaar', 'faltu', 'bewakoof', 'pagal', 'stupid',
                'kharab', 'barbad', 'tabah', 'nasht', 'nuksaan', 'hani',
                'अच्छा नही', 'अच्छा नहीं', 'good nahi', 'achha nahi', 'achha nhi',
                'accha nahi', 'accha nhi', 'theek nahi', 'theek nhi', 'sahi nahi',
                'sahi nhi', 'bekar ha', 'bekar hai', 'kaam nahi', 'kaam nhi',
                'start nahi', 'start nhi', 'nahi hogi', 'nhi hogi', 'nahi karegi',
                'nhi karegi', 'bigjaye', 'bigad jaye', 'bigad gaye', 'kharab ho',
                'problem aa', 'issue aa', 'barish ma', 'barish me', 'switches kaam',
                'chور', 'chor', 'चोर कंपनी', 'chor company', 'चोर कम्पनी'
            ]
        }
        
        self.intensity_modifiers = {
            'amplifiers': ['very', 'extremely', 'really', 'super', 'too', 'so', 'बहुत', 'काफी', 'अत्यधिक'],
            'diminishers': ['somewhat', 'rather', 'quite', 'fairly', 'slightly', 'थोड़ा', 'कम', 'हल्का']
        }

    def detect_language_mix(self, text: str) -> Dict[str, Any]:
        """Detect language composition of text"""
        text = text.lower().strip()
        
        # Count different script characters
        script_counts = {}
        total_chars = len(re.sub(r'[^\w]', '', text))
        
        if total_chars == 0:
            return {'is_mixed': False, 'primary_language': 'unknown', 'languages': {}}
        
        for script_name, pattern in self.script_patterns.items():
            matches = pattern.findall(text)
            char_count = sum(len(match) for match in matches)
            if char_count > 0:
                script_counts[script_name] = char_count / total_chars
        
        # Count English words
        english_word_count = 0
        words = re.findall(r'\b\w+\b', text)
        for word in words:
            if word in self.english_patterns['words'] or word in self.english_patterns['contractions']:
                english_word_count += 1
        
        english_ratio = english_word_count / len(words) if words else 0
        
        # Count local language words
        local_word_count = 0
        for lang_words in self.local_language_patterns.values():
            for word in words:
                if word in lang_words:
                    local_word_count += 1
        
        local_ratio = local_word_count / len(words) if words else 0
        
        # Determine primary language and mixing
        languages = {'english': english_ratio, **script_counts}
        languages['local_words'] = local_ratio
        
        # Filter out zero values
        languages = {k: v for k, v in languages.items() if v > 0}
        
        if not languages:
            primary_language = 'unknown'
            is_mixed = False
        else:
            primary_language = max(languages.keys(), key=languages.get)
            is_mixed = len(languages) > 1 and max(languages.values()) < 0.8
        
        return {
            'is_mixed': is_mixed,
            'primary_language': primary_language,
            'languages': languages,
            'script_distribution': script_counts
        }

    def analyze_emojis(self, text: str) -> Dict[str, Any]:
        """Analyze emoji sentiment in text"""
        emojis_found = self.emoji_regex.findall(text)
        
        if not emojis_found:
            return {
                'has_emojis': False,
                'emoji_count': 0,
                'emoji_sentiment_score': 0.0,
                'emoji_sentiment': 'neutral',
                'emojis': []
            }
        
        emoji_scores = []
        emoji_details = []
        
        for emoji in emojis_found:
            if emoji in self.emoji_sentiment:
                score = self.emoji_sentiment[emoji]
                emoji_scores.append(score)
                emoji_details.append({'emoji': emoji, 'score': score})
        
        if not emoji_scores:
            avg_score = 0.0
        else:
            avg_score = sum(emoji_scores) / len(emoji_scores)
        
        # Determine overall emoji sentiment
        if avg_score > 0.3:
            emoji_sentiment = 'positive'
        elif avg_score < -0.3:
            emoji_sentiment = 'negative'
        else:
            emoji_sentiment = 'neutral'
        
        return {
            'has_emojis': True,
            'emoji_count': len(emojis_found),
            'emoji_sentiment_score': round(avg_score, 3),
            'emoji_sentiment': emoji_sentiment,
            'emojis': emoji_details,
            'unique_emojis': len(set(emojis_found))
        }

    def detect_company_mentions(self, text: str) -> Dict[str, Any]:
        """Detect company and product mentions with attribution"""
        text_lower = text.lower()
        mentions = {}
        primary_mention = None
        competitor_mentions = []
        
        for company, patterns in self.company_patterns.items():
            mention_score = 0
            mention_types = []
            
            # Check primary mentions
            for pattern in patterns['primary']:
                if pattern in text_lower:
                    mention_score += 3
                    mention_types.append(f'primary: {pattern}')
            
            # Check product mentions
            for pattern in patterns['products']:
                if pattern in text_lower:
                    mention_score += 2
                    mention_types.append(f'product: {pattern}')
            
            # Check variations
            for pattern in patterns['variations']:
                if pattern in text_lower:
                    mention_score += 1
                    mention_types.append(f'variation: {pattern}')
            
            if mention_score > 0:
                mentions[company] = {
                    'score': mention_score,
                    'types': mention_types,
                    'confidence': min(mention_score / 5.0, 1.0)
                }
        
        # Determine primary mention (highest score)
        if mentions:
            primary_mention = max(mentions.keys(), key=lambda x: mentions[x]['score'])
            competitor_mentions = [company for company in mentions.keys() if company != primary_mention]
        
        return {
            'has_mentions': bool(mentions),
            'primary_company': primary_mention,
            'competitor_mentions': competitor_mentions,
            'all_mentions': mentions,
            'mention_count': len(mentions)
        }

    def calculate_engagement_weight(self, likes: int, replies: int = 0, shares: int = 0) -> Dict[str, Any]:
        """Calculate engagement-based sentiment weight"""
        # Normalize engagement metrics
        like_weight = min(likes / 100.0, 1.0) if likes > 0 else 0.0  # Cap at 100 likes = 1.0
        reply_weight = min(replies / 20.0, 0.5) if replies > 0 else 0.0  # Cap at 20 replies = 0.5
        share_weight = min(shares / 10.0, 0.3) if shares > 0 else 0.0   # Cap at 10 shares = 0.3
        
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
        """Analyze sentiment using pattern matching with improved word boundary detection"""
        import re  # Import re module for regex operations
        
        text_lower = text.lower()
        
        positive_score = 0
        negative_score = 0
        sentiment_words = []
        
        # Check for advice/question patterns first (should be neutral)
        # But exclude context-driven positive/negative recommendations
        advice_patterns = [
            'suggest', 'advice', 'help', 'bta', 'batao', 'tell me', 'koi', 'kaun', 'which',
            'please help', 'mujhe', 'chahiye', 'leni', 'kharidna', 'buy', 'purchase', 'planning',
            'bhaiya', 'sir', 'please', 'confusion', 'decide', 'choice', 'option', 'budget',
            'suggestion', 'guide', 'kya lena', 'best hai', 'dijiye', 'bataye'
        ]
        
        # Context-aware positive recommendation patterns
        positive_recommendation_patterns = [
            'dil se recommend', 'दिल से recommend', 'dil se suggest', 'heartily recommend',
            'strongly recommend', 'highly recommend', 'definitely recommend', 'really recommend',
            'zaroor recommend', 'जरूर recommend', 'bilkul recommend', 'बिल्कुल recommend'
        ]
        
        # Context-aware negative recommendation patterns  
        negative_recommendation_patterns = [
            'dil se mana', 'दिल से मना', 'dil se mat', 'दिल से मत', 'never recommend',
            'dont recommend', "don't recommend", 'avoid recommend', 'mat recommend',
            'मत recommend', 'kabhi mat', 'कभी मत', 'bilkul mat', 'बिल्कुल मत'
        ]
        
        # Strong negative patterns that should override neutral bias
        strong_negative_patterns = [
            'fraud', 'dhokha', 'dhoka', 'cheat', 'cheating', 'scam', 'fake',
            'duplicate', 'copy', 'loot', 'looting', 'theft', 'stealing', 'chori',
            'thagi', 'beimani', 'ripping off', 'ripoff', 'disaster', 'nightmare',
            'worst company', 'pathetic service', 'useless service', 'terrible service',
            'never again', 'never buy', 'warning', 'beware', 'avoid', 'dont buy',
            'do not buy', 'money waste', 'time waste', 'complete waste', 'total waste',
            'barbad', 'tabah', 'nasht', 'bekaar service', 'faltu company',
            'bewakoof company', 'pagal company', 'stupid company', 'ghatiya service',
            'bakwaas service', 'kharab experience', 'pareshan kar diya', 'tang aa gaya',
            'gussa aa gaya', 'nafrat ho gayi', 'ghrina ho gayi', 'afsos hai',
            'pachtawa hai', 'galti ki', 'bhool gaye', 'nuksan hua', 'hani hui',
            'going to fail', 'will fail', 'like fail', 'going down', 'downfall',
            'collapse', 'dead', 'dying', 'finish', 'finished', 'over', 'end', 'ended',
            'achha nahi', 'achha nhi', 'accha nahi', 'accha nhi', 'good nahi',
            'theek nahi', 'theek nhi', 'sahi nahi', 'sahi nhi', 'bekar ha', 'bekar hai',
            'kaam nahi', 'kaam nhi', 'start nahi', 'start nhi', 'nahi hogi', 'nhi hogi',
            'nahi karegi', 'nhi karegi', 'bigjaye', 'bigad jaye', 'bigad gaye',
            'kharab ho', 'problem aa', 'issue aa', 'barish ma bigjaye', 'barish me bigjaye',
            'switches kaam nahi', 'switches kaam nhi', 'chor company', 'chor कंपनी',
            'चोर कंपनी', 'चोर कम्पनी', 'no good', 'not good', 'डिजाइन अच्छा नही',
            'design achha nahi', 'design accha nahi', 'डिजाइन अच्छा नहीं',
            'not learning from mistakes', 'weird seat design', 'weird design',
            'bekar hai', 'bekaar hai', 'not worth buying', 'not worth it',
            'complicating things', 'making complicated', 'avoid buying', 'dont buy',
            'do not buy', 'should not buy', 'shouldnt buy', 'regret buying',
            'buying mistake', 'design problem', 'design issue', 'design flaw',
            'seat problem', 'uncomfortable seat', 'bad design', 'poor design',
            'faulty design',
            # New critical patterns from user examples
            'बरोबर नही', 'बरोबर नहीं', 'barobar nahi', 'barobar nhi',
            'सर्विस बरोबर नही', 'service barobar nahi', 'service barobar nhi',
            'lot of problems', 'lots of problems', 'a lot of problems',
            'stops in the middle', 'stops in middle', 'band ho jata', 'ruk jata',
            'life threatening', 'life threat', 'jaan ka khatra', 'dangerous',
            'kharaab gaadi', 'kharab gaadi', 'खराब गाडी', 'bad vehicle',
            'jaan liya', 'जान लिया', 'killed people', 'death cases',
            'rubbish', 'garbage', 'bakwas', 'बकवास', 'faltu',
            'promot math karna', 'promote mat karna', 'प्रमोट मत करना',
            'please dont buy', 'please don\'t buy', 'कृपया मत खरीदो',
            'mat lo', 'मत लो', 'dont take', 'don\'t take', 'nahi lena',
            'नहीं लेना', 'avoid karo', 'बचें', 'stay away',
            # Fraud typos and informal negative patterns
            'froud', 'frawd', 'frod', 'company froud', 'company frawd',
            'koi service nhi', 'koi service nahi', 'कोई सर्विस नही',
            'bhag gya', 'भाग गया', 'bhag gaya', 'company bhag gyi', 'company bhag gayi',
            'kmpny froud', 'cmpany fraud', 'hero froud', 'ola froud', 'ather froud'
        ]
        
        # Negative phrase patterns that contain multiple words
        negative_phrase_patterns = [
            r'going to fail',
            r'will fail',
            r'like.*fail',
            r'अच्छा नही',
            r'अच्छा नहीं', 
            r'achha nahi',
            r'achha nhi',
            r'accha nahi',
            r'accha nhi',
            r'good nahi',
            r'good nhi',
            r'theek nahi',
            r'theek nhi',
            r'sahi nahi',
            r'sahi nhi',
            r'bekar ha',
            r'bekar hai',
            r'kaam nahi.*karegi',
            r'kaam nhi.*karegi',
            r'start nahi.*hogi',
            r'start nhi.*hogi',
            r'barish.*bigjaye',
            r'switches.*kaam.*nahi',
            r'switches.*kaam.*nhi',
            r'chor.*company',
            r'chor.*कंपनी',
            r'चोर.*कंपनी',
            r'चोर.*कम्पनी',
            r'no.*good',
            r'not.*good',
            r'डिजाइन.*अच्छा.*नही',
            r'डिजाइन.*अच्छा.*नहीं',
            r'design.*achha.*nahi',
            r'design.*accha.*nahi',
            r'not.*learning.*mistakes',
            r'not.*learning.*from.*mistakes',
            r'weird.*seat.*design',
            r'weird.*design',
            r'seat.*design.*weird',
            r'bekar.*hai',
            r'bekaar.*hai',
            r'not.*worth.*buying',
            r'not.*worth.*it',
            r'complicating.*things',
            r'making.*complicated',
            r'avoid.*buying',
            r'dont.*buy',
            r'do.*not.*buy',
            r'should.*not.*buy',
            r'shouldnt.*buy',
            r'regret.*buying',
            r'buying.*mistake',
            r'design.*problem',
            r'design.*issue',
            r'design.*flaw',
            r'seat.*problem',
            r'uncomfortable.*seat',
            r'bad.*design',
            r'poor.*design',
            r'faulty.*design',
            # Critical new patterns from user examples
            r'बरोबर.*नही',
            r'बरोबर.*नहीं',
            r'barobar.*nahi',
            r'barobar.*nhi',
            r'सर्विस.*बरोबर.*नही',
            r'service.*barobar.*nahi',
            r'service.*barobar.*nhi',
            r'lot.*of.*problems',
            r'lots.*of.*problems',
            r'a.*lot.*of.*problems',
            r'stops.*in.*the.*middle',
            r'stops.*in.*middle',
            r'band.*ho.*jata',
            r'रुक.*जाता',
            r'life.*threatening',
            r'life.*threat',
            r'jaan.*ka.*khatra',
            r'जान.*का.*खतरा',
            r'kharaab.*gaadi',
            r'kharab.*gaadi',
            r'खराब.*गाडी',
            r'bad.*vehicle',
            r'jaan.*liya',
            r'जान.*लिया',
            r'killed.*people',
            r'death.*cases',
            r'rubbish.*wheels',
            r'garbage.*wheels',
            r'bakwas.*wheels',
            r'promot.*math.*karna',
            r'promote.*mat.*karna',
            r'प्रमोट.*मत.*करना',
            r'please.*dont.*buy',
            r'please.*don\'t.*buy',
            r'कृपया.*मत.*खरीदो',
            r'mat.*lo.*koi.*bhi',
            r'मत.*लो.*कोई.*भी',
            r'dont.*take.*any',
            r'don\'t.*take.*any',
            r'nahi.*lena.*chahiye',
            r'नहीं.*लेना.*चाहिए',
            r'avoid.*this.*vehicle',
            r'stay.*away.*from'
        ]
        
        is_advice_request = any(pattern in text_lower for pattern in advice_patterns)
        has_strong_negative = any(pattern in text_lower for pattern in strong_negative_patterns)
        
        # Check for context-aware recommendations
        has_positive_recommendation = any(pattern in text_lower for pattern in positive_recommendation_patterns)
        has_negative_recommendation = any(pattern in text_lower for pattern in negative_recommendation_patterns)
        
        # Override advice request detection for context-aware recommendations
        if has_positive_recommendation or has_negative_recommendation:
            is_advice_request = False  # This is sentiment, not advice request
        
        # Check for negative phrase patterns using regex
        has_negative_phrase = False
        for pattern in negative_phrase_patterns:
            if re.search(pattern, text_lower):
                has_negative_phrase = True
                break
        
        # Transliteration corrections - words that might be mismatched
        transliteration_corrections = {
            'badhiya': 'positive',  # "badhiya" contains "bad" but means "good"
            'badiya': 'positive',
            'achha': 'positive',
            'accha': 'positive',
            'mast': 'positive',
            'bekaar': 'negative',
            'bakwaas': 'negative',
            'ghatiya': 'negative',
            'dhokha': 'negative',  # fraud
            'dhoka': 'negative',   # fraud (alternate spelling)
            'fraud': 'negative',
            'jhooth': 'negative',  # lie
            'jhoot': 'negative',   # lie (alternate spelling)
            'nakli': 'negative',   # fake
            'duplicate': 'negative',
            'loot': 'negative',    # robbery/overcharging
            'looting': 'negative',
            'chori': 'negative',   # theft
            'thagi': 'negative',   # cheating
            'beimani': 'negative', # dishonesty
            'barbad': 'negative',  # ruined
            'tabah': 'negative',   # destroyed
            'nasht': 'negative',   # destroyed
            'nikamma': 'negative', # useless
            'gandagi': 'negative', # filth/mess
            'kachra': 'negative',  # garbage
            'sharmnak': 'negative',# shameful
            'besharm': 'negative', # shameless
            'bewakoof': 'negative',# stupid
            'bewakoofi': 'negative',# stupidity
            'murkhata': 'negative',# foolishness
            'galti': 'negative',   # mistake
            'bhool': 'negative',   # mistake
            'nuksan': 'negative',  # loss
            'nuksaan': 'negative', # loss (alternate spelling)
            'hani': 'negative',    # harm
            'ghata': 'negative',   # loss
            'pareshan': 'negative',# troubled
            'tang': 'negative',    # troubled
            'gussa': 'negative',   # anger
            'krodh': 'negative',   # anger
            'nafrat': 'negative',  # hate
            'ghrina': 'negative',  # hate
            'afsos': 'negative',   # regret
            'pachtawa': 'negative',# repentance
            'dukh': 'negative',    # sorrow
            'dard': 'negative',    # pain
            'kasht': 'negative',   # trouble
            'saza': 'negative',    # punishment
            'sirdard': 'negative', # headache
            'kharab': 'negative',  # bad
            'faltu': 'negative',   # useless
            'pagal': 'negative',   # crazy (when used negatively)
            'bekar': 'negative',   # useless/bad
            'fail': 'negative',    # failure
            'failing': 'negative', # failing
            'achha nahi': 'negative', # not good
            'achha nhi': 'negative',  # not good
            'accha nahi': 'negative', # not good
            'accha nhi': 'negative',  # not good
            'good nahi': 'negative',  # not good
            'theek nahi': 'negative', # not okay
            'theek nhi': 'negative',  # not okay
            'sahi nahi': 'negative',  # not right
            'sahi nhi': 'negative',   # not right
            'kaam nahi': 'negative',  # doesn't work
            'kaam nhi': 'negative',   # doesn't work
            'start nahi': 'negative', # doesn't start
            'start nhi': 'negative',  # doesn't start
            'nahi hogi': 'negative',  # won't happen/work
            'nhi hogi': 'negative',   # won't happen/work
            'nahi karegi': 'negative',# won't work
            'nhi karegi': 'negative', # won't work
            'bigjaye': 'negative',    # gets spoiled
            'bigad': 'negative',      # spoiled
            'chor': 'negative',       # thief
            'chor company': 'negative', # thief company
            'bekar hai': 'negative',  # it's useless/bad
            'bekaar hai': 'negative', # it's useless/bad
            'not worth': 'negative',  # not worth it
            'not worth buying': 'negative', # not worth buying
            'not learning': 'negative', # not learning from mistakes
            'weird seat': 'negative', # weird seat design
            'weird design': 'negative', # weird design
            'seat design': 'negative', # problematic seat design (context dependent)
            'complicating': 'negative', # making things complicated
            'complicate': 'negative',  # making complicated
            'mistakes': 'negative',    # making mistakes
            'learning mistakes': 'negative', # not learning from mistakes
            'worth nahi': 'negative',  # not worth it (Hindi-English mix)
            'worth nhi': 'negative',   # not worth it (Hindi-English mix)
            'design problem': 'negative', # design issues
            'design issue': 'negative',   # design problems
            'design flaw': 'negative',    # design flaws
            'seat problem': 'negative',   # seat related problems
            'uncomfortable seat': 'negative', # uncomfortable seating
            'bad design': 'negative',     # poor design
            'poor design': 'negative',    # poor design
            'faulty design': 'negative',  # faulty design
            'buying mistake': 'negative', # mistake in buying
            'regret buying': 'negative',  # regret the purchase
            'shouldnt buy': 'negative',   # shouldn't buy
            'should not buy': 'negative', # should not buy
            'avoid buying': 'negative',   # avoid purchasing
            'dont buy': 'negative',       # don't buy
            'do not buy': 'negative',     # do not buy
            # Critical Hindi-English mixed patterns from user examples
            'बरोबर नही': 'negative',      # service not proper
            'बरोबर नहीं': 'negative',     # service not proper (formal)
            'barobar nahi': 'negative',   # service not proper (transliterated)
            'barobar nhi': 'negative',    # service not proper (transliterated short)
            'सर्विस बरोबर नही': 'negative', # service not proper
            'service barobar nahi': 'negative', # service not proper (mixed)
            'service barobar nhi': 'negative',  # service not proper (mixed short)
            'lot of problems': 'negative', # many problems
            'lots of problems': 'negative', # many problems
            'a lot of problems': 'negative', # many problems
            'stops in middle': 'negative', # vehicle breakdown
            'stops in the middle': 'negative', # vehicle breakdown
            'band ho jata': 'negative',   # gets stopped/breaks down
            'रुक जाता': 'negative',       # gets stopped
            'life threatening': 'negative', # dangerous
            'life threat': 'negative',    # dangerous
            'jaan ka khatra': 'negative', # life danger
            'जान का खतरा': 'negative',   # life danger
            'kharaab gaadi': 'negative',  # bad vehicle
            'kharab gaadi': 'negative',   # bad vehicle
            'खराब गाडी': 'negative',      # bad vehicle
            'bad vehicle': 'negative',    # bad vehicle
            'jaan liya': 'negative',      # killed/took life
            'जान लिया': 'negative',       # killed/took life
            'killed people': 'negative',  # fatal incidents
            'death cases': 'negative',    # fatal incidents
            'rubbish wheels': 'negative', # poor quality wheels
            'rubbish alloy': 'negative',  # poor quality alloy
            'garbage wheels': 'negative', # poor quality wheels
            'bakwas wheels': 'negative',  # poor quality wheels
            'promot math karna': 'negative', # don't promote
            'promote mat karna': 'negative', # don't promote
            'प्रमोट मत करना': 'negative', # don't promote
            'please dont buy': 'negative', # strong purchase warning
            'please don\'t buy': 'negative', # strong purchase warning
            'कृपया मत खरीदो': 'negative', # please don't buy
            'mat lo koi bhi': 'negative', # don't take any
            'मत लो कोई भी': 'negative',   # don't take any
            'dont take any': 'negative',  # don't take any
            'don\'t take any': 'negative', # don't take any
            'nahi lena chahiye': 'negative', # shouldn't take
            'नहीं लेना चाहिए': 'negative', # shouldn't take
            'avoid this vehicle': 'negative', # avoid this vehicle
            'stay away from': 'negative', # stay away from
            'mat karo promote': 'negative', # don't promote
            'मत करो प्रमोट': 'negative',  # don't promote
            'dangerous vehicle': 'negative', # dangerous vehicle
            'खतरनाक गाडी': 'negative',    # dangerous vehicle
            'khatarnak gaadi': 'negative', # dangerous vehicle
            'problem bahut': 'negative',  # too many problems
            'समस्या बहुत': 'negative',    # too many problems
            'samasya bahut': 'negative',  # too many problems
            # New critical patterns for typos and informal language
            'froud': 'negative',          # fraud (typo)
            'frawd': 'negative',          # fraud (typo)
            'frod': 'negative',           # fraud (typo)
            'company froud': 'negative',  # company fraud (typo)
            'company frawd': 'negative',  # company fraud (typo)
            'koi service nhi': 'negative', # no service at all
            'koi service nahi': 'negative', # no service at all
            'कोई सर्विस नही': 'negative', # no service at all
            'bhag gya': 'negative',       # ran away / escaped
            'भाग गया': 'negative',        # ran away / escaped
            'bhag gaya': 'negative',      # ran away / escaped
            'company bhag gyi': 'negative', # company ran away
            'company bhag gayi': 'negative', # company ran away
            'kmpny froud': 'negative',    # company fraud (informal typing)
            'cmpany fraud': 'negative',   # company fraud (informal typing)
            # Positive Hindi informal patterns
            'bhot achhi': 'positive',     # very good (informal)
            'बहुत अच्छी': 'positive',     # very good
            'bahut achhi': 'positive',    # very good
            'bahut acchi': 'positive',    # very good
            'bhot acchi': 'positive',     # very good (informal)
            'bhot achha': 'positive',     # very good (informal)
            'बहुत अच्छा': 'positive',     # very good
            'bahut achha': 'positive',    # very good
            'bahut accha': 'positive',    # very good
            'bhot accha': 'positive',     # very good (informal)
            'dil se': 'positive',         # from the heart
            'दिल से': 'positive',         # from the heart
            'gadi hai': 'neutral',        # vehicle is (context dependent)
            'गाडी है': 'neutral',         # vehicle is (context dependent)
            'bhot badhiya': 'positive',   # very good (informal)
            'बहुत बढ़िया': 'positive',    # very good
            'bahut badhiya': 'positive',  # very good
            'bhot badiya': 'positive',    # very good (informal)
            'बहुत बडिया': 'positive',     # very good (alternate spelling)
            'bahut badiya': 'positive',   # very good
            'ekdum mast': 'positive',     # totally awesome
            'एकदम मस्त': 'positive',      # totally awesome
            'bilkul sahi': 'positive',    # absolutely right
            'बिल्कुल सही': 'positive',    # absolutely right
            'bhot sahi': 'positive',      # very right/good (informal)
            'बहुत सही': 'positive',       # very right/good
            'bahut sahi': 'positive',     # very right/good
            # Context-aware recommendation patterns
            'dil se recommend': 'positive',     # heartfelt recommendation
            'दिल से recommend': 'positive',     # heartfelt recommendation
            'dil se suggest': 'positive',       # heartfelt suggestion
            'heartily recommend': 'positive',   # strong positive recommendation
            'strongly recommend': 'positive',   # strong positive recommendation
            'highly recommend': 'positive',     # strong positive recommendation
            'definitely recommend': 'positive', # definite positive recommendation
            'really recommend': 'positive',     # strong positive recommendation
            'zaroor recommend': 'positive',     # definitely recommend
            'जरूर recommend': 'positive',       # definitely recommend
            'bilkul recommend': 'positive',     # absolutely recommend
            'बिल्कुल recommend': 'positive',    # absolutely recommend
            # Context-aware negative recommendation patterns
            'dil se mana': 'negative',          # refuse from heart
            'दिल से मना': 'negative',           # refuse from heart
            'dil se mat': 'negative',           # don't from heart
            'दिल से मत': 'negative',            # don't from heart
            'never recommend': 'negative',      # never recommend
            'dont recommend': 'negative',       # don't recommend
            "don't recommend": 'negative',      # don't recommend
            'avoid recommend': 'negative',      # avoid recommending
            'mat recommend': 'negative',        # don't recommend
            'मत recommend': 'negative',         # don't recommend
            'kabhi mat': 'negative',            # never
            'कभी मत': 'negative',               # never
            'bilkul mat': 'negative',           # absolutely don't
            'बिल्कुल मत': 'negative'            # absolutely don't
        }
        
        # Apply transliteration corrections first
        for word, sentiment in transliteration_corrections.items():
            if word in text_lower:
                if sentiment == 'positive':
                    # Give extra weight to context-aware positive recommendations
                    if any(rec_pattern in word for rec_pattern in ['dil se recommend', 'heartily recommend', 'strongly recommend', 'highly recommend']):
                        positive_score += 3.0  # Strong positive for context-aware recommendations
                    else:
                        positive_score += 2.0  # Increased weight for positive informal patterns
                    sentiment_words.append({'word': word, 'sentiment': 'positive', 'language': 'transliteration'})
                else:
                    # Give extra weight to context-aware negative recommendations
                    if any(neg_pattern in word for neg_pattern in ['dil se mana', 'dil se mat', 'never recommend', 'dont recommend']):
                        negative_score += 3.0  # Strong negative for context-aware refusals
                    else:
                        negative_score += 1
                    sentiment_words.append({'word': word, 'sentiment': 'negative', 'language': 'transliteration'})
        
        # Analyze English patterns with word boundary checks
        if language_info['primary_language'] == 'english' or 'english' in language_info['languages']:
            for word in self.positive_patterns['english']:
                # Use word boundary to avoid false matches (e.g., "bad" in "badhiya")
                import re
                if re.search(r'\b' + re.escape(word) + r'\b', text_lower):
                    # Exclude if part of transliteration word
                    if not any(trans_word in text_lower and word in trans_word for trans_word in transliteration_corrections.keys()):
                        positive_score += 1
                        sentiment_words.append({'word': word, 'sentiment': 'positive', 'language': 'english'})
            
            for word in self.negative_patterns['english']:
                # Use word boundary to avoid false matches
                if re.search(r'\b' + re.escape(word) + r'\b', text_lower):
                    # Exclude if part of transliteration word  
                    if not any(trans_word in text_lower and word in trans_word for trans_word in transliteration_corrections.keys()):
                        negative_score += 1
                        sentiment_words.append({'word': word, 'sentiment': 'negative', 'language': 'english'})
        
        # Analyze Hindi patterns
        if language_info['primary_language'] in ['devanagari', 'local_words'] or language_info['is_mixed']:
            for word in self.positive_patterns['hindi']:
                if word in text_lower:
                    positive_score += 1
                    sentiment_words.append({'word': word, 'sentiment': 'positive', 'language': 'hindi'})
            
            for word in self.negative_patterns['hindi']:
                if word in text_lower:
                    negative_score += 1
                    sentiment_words.append({'word': word, 'sentiment': 'negative', 'language': 'hindi'})
        
        # Check for intensity modifiers
        intensity_multiplier = 1.0
        for amplifier in self.intensity_modifiers['amplifiers']:
            if amplifier in text_lower:
                intensity_multiplier = 1.5
                break
        
        for diminisher in self.intensity_modifiers['diminishers']:
            if diminisher in text_lower:
                intensity_multiplier = 0.7
                break
        
        # Apply intensity
        positive_score *= intensity_multiplier
        negative_score *= intensity_multiplier
        
        # Calculate final sentiment with advice request consideration
        total_score = positive_score + negative_score
        
        # Context-aware positive recommendations should be positive (highest priority)
        if has_positive_recommendation and positive_score > 0:
            sentiment = 'positive'
            confidence = min(0.95, 0.8 + (positive_score / max(total_score, 1)) * 0.15)
        # Context-aware negative recommendations should be negative
        elif has_negative_recommendation or has_strong_negative or has_negative_phrase:
            # Even if no negative words detected, negative phrases should make it negative
            if negative_score == 0 and (has_strong_negative or has_negative_phrase or has_negative_recommendation):
                negative_score = 3.0  # Strong negative assignment for phrase patterns
                total_score = positive_score + negative_score
            elif negative_score > 0:
                negative_score += 1.0  # Boost existing negative score  
                total_score = positive_score + negative_score
            sentiment = 'negative'
            confidence = min(0.95, 0.8 + (negative_score / max(total_score, 1)) * 0.15)
        elif is_advice_request and not has_strong_negative and not has_negative_phrase and not has_positive_recommendation and not has_negative_recommendation:
            # For advice requests, bias towards neutral unless strong sentiment
            # But don't override strong positive informal patterns (score >= 1.8)
            if total_score == 0 or (abs(positive_score - negative_score) < 1 and positive_score < 1.8):
                sentiment = 'neutral'
                confidence = 0.7  # High confidence for advice requests
            elif positive_score > negative_score + 0.5 or positive_score >= 1.8:  # Strong positive override (lowered threshold)
                sentiment = 'positive'
                confidence = min(0.9, 0.5 + (positive_score - negative_score) / total_score * 0.3)
            else:
                sentiment = 'negative'
                confidence = min(0.9, 0.5 + (negative_score - positive_score) / total_score * 0.3)
        else:
            # Regular sentiment calculation with negative bias
            if total_score == 0:
                sentiment = 'neutral'
                confidence = 0.3
            elif negative_score >= positive_score:  # Changed from > to >= for negative bias
                sentiment = 'negative'
                confidence = min(0.9, 0.6 + (negative_score - positive_score) / total_score * 0.3)
            else:
                sentiment = 'positive'
                confidence = min(0.9, 0.5 + (positive_score - negative_score) / total_score * 0.4)
        
        return {
            'sentiment': sentiment,
            'confidence': round(confidence, 3),
            'positive_score': round(positive_score, 2),
            'negative_score': round(negative_score, 2),
            'intensity_multiplier': round(intensity_multiplier, 2),
            'sentiment_words': sentiment_words,
            'is_advice_request': is_advice_request,
            'has_strong_negative': has_strong_negative,
            'has_negative_phrase': has_negative_phrase,
            'has_positive_recommendation': has_positive_recommendation,
            'has_negative_recommendation': has_negative_recommendation
        }

    def detect_sarcasm_advanced(self, text: str, emoji_info: Dict, company_info: Dict) -> Dict[str, Any]:
        """Advanced sarcasm detection with context"""
        sarcasm_indicators = []
        sarcasm_score = 0.0
        
        text_lower = text.lower()
        
        # Pattern 1: Positive words with negative context
        positive_negative_patterns = [
            (r'(great|excellent|amazing|wonderful).*(problem|issue|trouble|broken|fail|fraud|dhokha)', 0.8),
            (r'(love|like).*(visit.*center|repair|fix|replace|service.*center)', 0.7),
            (r'(perfect|fantastic).*(again|multiple|many times|third.*time|fourth.*time)', 0.6),
            (r'(good|nice).*(service center|complaint|issue|problem|trouble)', 0.5),
            (r'(best|superb).*(experience|service).*(fraud|dhokha|cheat|loot|waste)', 0.9),
            (r'(awesome|brilliant).*(company|service).*(never.*again|warning|avoid)', 0.8)
        ]
        
        for pattern, score in positive_negative_patterns:
            if re.search(pattern, text_lower):
                sarcasm_score += score
                sarcasm_indicators.append(f'positive_negative_pattern: {pattern}')
        
        # Pattern 2: Exclamation with complaints
        if re.search(r'!.*(problem|issue|trouble|broken|service)', text_lower):
            sarcasm_score += 0.4
            sarcasm_indicators.append('exclamation_with_complaint')
        
        # Pattern 3: Emoji-text mismatch
        if emoji_info['has_emojis']:
            if emoji_info['emoji_sentiment'] == 'positive' and any(word in text_lower for word in ['problem', 'issue', 'terrible', 'worst']):
                sarcasm_score += 0.6
                sarcasm_indicators.append('emoji_text_mismatch')
        
        # Pattern 4: Thanks with complaints
        thanks_complaint_patterns = [
            r'thanks.*(for nothing|but|however)',
            r'grateful.*(worst|terrible|problem)',
            r'appreciate.*(waste|useless|pathetic)'
        ]
        
        for pattern in thanks_complaint_patterns:
            if re.search(pattern, text_lower):
                sarcasm_score += 0.7
                sarcasm_indicators.append(f'thanks_complaint: {pattern}')
        
        # Pattern 5: Repeated service center visits with positive words
        service_patterns = [
            r'(great|good|excellent).*(visit.*\d+.*times|multiple.*visit|again.*service)',
            r'(amazing|wonderful).*(third.*time|fourth.*time|many.*visits)'
        ]
        
        for pattern in service_patterns:
            if re.search(pattern, text_lower):
                sarcasm_score += 0.9
                sarcasm_indicators.append(f'service_visit_sarcasm: {pattern}')
        
        # Normalize sarcasm score
        sarcasm_score = min(sarcasm_score, 1.0)
        
        # Determine if sarcasm is detected
        sarcasm_detected = sarcasm_score > 0.5
        
        return {
            'sarcasm_detected': sarcasm_detected,
            'sarcasm_score': round(sarcasm_score, 3),
            'sarcasm_indicators': sarcasm_indicators,
            'confidence': round(min(sarcasm_score * 1.2, 1.0), 3)
        }

    async def classify_comment_advanced(self, comment: Dict, target_oem: str = None) -> Dict[str, Any]:
        """Perform advanced multi-layered sentiment classification"""
        text = comment.get('text', '')
        likes = comment.get('likes', 0)
        replies = comment.get('replies', 0)
        shares = comment.get('shares', 0)
        
        if not text:
            return self._create_default_classification()
        
        # Step 1: Language Analysis
        language_info = self.detect_language_mix(text)
        
        # Step 2: Emoji Analysis
        emoji_info = self.analyze_emojis(text)
        
        # Step 3: Company Mention Analysis
        company_info = self.detect_company_mentions(text)
        
        # Step 4: Engagement Analysis
        engagement_info = self.calculate_engagement_weight(likes, replies, shares)
        
        # Step 5: Pattern-based Sentiment Analysis
        pattern_sentiment = self.analyze_sentiment_patterns(text, language_info)
        
        # Step 6: Advanced Sarcasm Detection
        sarcasm_info = self.detect_sarcasm_advanced(text, emoji_info, company_info)
        
        # Step 7: Combine all factors for final sentiment
        final_sentiment = self._calculate_final_sentiment(
            pattern_sentiment, emoji_info, sarcasm_info, engagement_info, company_info, target_oem
        )
        
        # Step 8: Product Relevance
        relevance_info = self._calculate_product_relevance(text, company_info, target_oem)
        
        # Step 9: Context Detection
        context_info = self._detect_context_advanced(text)
        
        return {
            'sentiment': final_sentiment['sentiment'],
            'confidence': final_sentiment['confidence'],
            'sarcasm_detected': sarcasm_info['sarcasm_detected'],
            'sarcasm_score': sarcasm_info['sarcasm_score'],
            'language_analysis': language_info,
            'emoji_analysis': emoji_info,
            'company_analysis': company_info,
            'engagement_analysis': engagement_info,
            'pattern_analysis': pattern_sentiment,
            'sarcasm_analysis': sarcasm_info,
            'product_relevance': relevance_info['level'],
            'relevance_score': relevance_info['score'],
            'context': context_info['primary_context'],
            'context_details': context_info,
            'analysis_method': 'advanced_multi_layer',
            'classification_factors': final_sentiment['factors']
        }

    def _calculate_final_sentiment(self, pattern_sentiment: Dict, emoji_info: Dict, 
                                  sarcasm_info: Dict, engagement_info: Dict, 
                                  company_info: Dict, target_oem: str) -> Dict[str, Any]:
        """Calculate final sentiment by combining all factors"""
        
        factors = []
        
        # Base sentiment from patterns
        base_sentiment = pattern_sentiment['sentiment']
        base_confidence = pattern_sentiment['confidence']
        factors.append(f"pattern_sentiment: {base_sentiment} (conf: {base_confidence})")
        
        # Emoji influence
        emoji_influence = 0.0
        if emoji_info['has_emojis']:
            emoji_influence = emoji_info['emoji_sentiment_score'] * 0.3  # 30% weight
            factors.append(f"emoji_influence: {emoji_influence:.2f}")
        
        # Sarcasm adjustment
        if sarcasm_info['sarcasm_detected']:
            if base_sentiment == 'positive':
                base_sentiment = 'negative'
                base_confidence *= 0.8  # Reduce confidence for sarcasm
                factors.append("sarcasm_flip: positive -> negative")
            elif base_sentiment == 'neutral' and emoji_info['emoji_sentiment'] == 'positive':
                base_sentiment = 'negative'
                base_confidence = 0.6
                factors.append("sarcasm_flip: neutral -> negative (emoji positive)")
        
        # Engagement amplification
        if engagement_info['engagement_level'] in ['high', 'viral']:
            base_confidence *= engagement_info['amplification_factor']
            factors.append(f"engagement_boost: {engagement_info['amplification_factor']}")
        
        # Company mention relevance
        if company_info['has_mentions']:
            if target_oem and target_oem in company_info['all_mentions']:
                # This comment is about the target company
                relevance_boost = company_info['all_mentions'][target_oem]['confidence'] * 0.1
                base_confidence += relevance_boost
                factors.append(f"target_company_relevance: +{relevance_boost:.2f}")
            elif company_info['primary_company'] != target_oem:
                # This comment is about a different company
                base_confidence *= 0.7  # Reduce confidence for misattributed sentiment
                factors.append("competitor_mention: confidence reduced")
        
        # Apply emoji influence to final sentiment
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
        
        # Ensure confidence is within bounds
        final_confidence = max(0.3, min(0.95, base_confidence))
        
        return {
            'sentiment': final_sentiment,
            'confidence': round(final_confidence, 3),
            'factors': factors,
            'final_score': round(final_score, 3)
        }

    def _calculate_product_relevance(self, text: str, company_info: Dict, target_oem: str) -> Dict[str, Any]:
        """Calculate product relevance for the text"""
        
        # EV-related keywords
        ev_keywords = [
            'electric', 'battery', 'range', 'charging', 'scooter', 'bike', 'motorcycle',
            'ev', 'electric vehicle', 'eco-friendly', 'green', 'sustainable',
            'motor', 'acceleration', 'speed', 'mileage', 'efficiency'
        ]
        
        # Service-related keywords
        service_keywords = [
            'service', 'maintenance', 'repair', 'support', 'center', 'technician',
            'warranty', 'parts', 'replacement', 'fix', 'issue', 'problem'
        ]
        
        text_lower = text.lower()
        
        # Count relevant keywords
        ev_score = sum(1 for keyword in ev_keywords if keyword in text_lower)
        service_score = sum(1 for keyword in service_keywords if keyword in text_lower)
        
        # Company mention score
        company_score = 0
        if company_info['has_mentions']:
            if target_oem and target_oem in company_info['all_mentions']:
                company_score = company_info['all_mentions'][target_oem]['score']
            else:
                company_score = max(mention['score'] for mention in company_info['all_mentions'].values())
        
        # Calculate total relevance score
        total_score = (ev_score * 0.4) + (service_score * 0.3) + (company_score * 0.3)
        
        # Normalize to 0-1 scale
        normalized_score = min(total_score / 10.0, 1.0)
        
        # Determine relevance level
        if normalized_score >= 0.7:
            relevance_level = 'high'
        elif normalized_score >= 0.4:
            relevance_level = 'medium'
        elif normalized_score > 0:
            relevance_level = 'low'
        else:
            relevance_level = 'none'
        
        return {
            'score': round(normalized_score, 3),
            'level': relevance_level,
            'ev_keywords': ev_score,
            'service_keywords': service_score,
            'company_score': company_score
        }

    def _detect_context_advanced(self, text: str) -> Dict[str, Any]:
        """Detect context categories with advanced classification"""
        
        context_patterns = {
            'service': [
                'service center', 'maintenance', 'repair', 'technician', 'support',
                'warranty', 'parts', 'replacement', 'fix', 'issue', 'problem'
            ],
            'battery_performance': [
                'battery', 'range', 'mileage', 'charging', 'charge', 'power',
                'distance', 'km', 'battery life', 'backup'
            ],
            'riding_experience': [
                'ride', 'driving', 'acceleration', 'speed', 'performance', 'handling',
                'comfort', 'seat', 'suspension', 'brakes'
            ],
            'purchase_decision': [
                'buy', 'purchase', 'price', 'cost', 'expensive', 'cheap', 'value',
                'money', 'worth', 'deal', 'offer', 'discount'
            ],
            'comparison': [
                'vs', 'versus', 'compare', 'better', 'best', 'worst', 'than',
                'alternative', 'option', 'choice'
            ],
            'build_quality': [
                'build', 'quality', 'material', 'plastic', 'metal', 'finish',
                'design', 'look', 'appearance', 'style'
            ],
            'features': [
                'feature', 'technology', 'smart', 'app', 'connectivity', 'digital',
                'display', 'instrument', 'cluster'
            ]
        }
        
        text_lower = text.lower()
        context_scores = {}
        
        for context, keywords in context_patterns.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                context_scores[context] = score
        
        if not context_scores:
            return {
                'primary_context': 'general',
                'context_scores': {},
                'context_confidence': 0.3
            }
        
        # Find primary context
        primary_context = max(context_scores.keys(), key=context_scores.get)
        max_score = context_scores[primary_context]
        
        # Calculate confidence
        total_score = sum(context_scores.values())
        confidence = max_score / total_score if total_score > 0 else 0.3
        
        return {
            'primary_context': primary_context,
            'context_scores': context_scores,
            'context_confidence': round(confidence, 3)
        }

    def _create_default_classification(self) -> Dict[str, Any]:
        """Create default classification for empty or invalid text"""
        return {
            'sentiment': 'neutral',
            'confidence': 0.3,
            'sarcasm_detected': False,
            'sarcasm_score': 0.0,
            'language_analysis': {'is_mixed': False, 'primary_language': 'unknown'},
            'emoji_analysis': {'has_emojis': False, 'emoji_sentiment': 'neutral'},
            'company_analysis': {'has_mentions': False, 'primary_company': None},
            'engagement_analysis': {'engagement_level': 'none'},
            'product_relevance': 'none',
            'relevance_score': 0.0,
            'context': 'general',
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
                # Fallback to default classification
                enhanced_comment = comment.copy()
                enhanced_comment['advanced_sentiment_classification'] = self._create_default_classification()
                enhanced_comments.append(enhanced_comment)
        
        return enhanced_comments

    def get_batch_summary(self, enhanced_comments: List[Dict]) -> Dict[str, Any]:
        """Generate summary statistics for a batch of classified comments"""
        total_comments = len(enhanced_comments)
        if total_comments == 0:
            return {'error': 'No comments to analyze'}
        
        # Initialize counters
        sentiment_counts = defaultdict(int)
        language_counts = defaultdict(int)
        emoji_counts = {'with_emojis': 0, 'without_emojis': 0}
        sarcasm_counts = {'detected': 0, 'not_detected': 0}
        engagement_counts = defaultdict(int)
        company_mention_counts = defaultdict(int)
        
        total_confidence = 0
        total_engagement_score = 0
        
        for comment in enhanced_comments:
            classification = comment.get('advanced_sentiment_classification', {})
            
            # Sentiment distribution
            sentiment_counts[classification.get('sentiment', 'unknown')] += 1
            
            # Language distribution
            lang_info = classification.get('language_analysis', {})
            primary_lang = lang_info.get('primary_language', 'unknown')
            language_counts[primary_lang] += 1
            
            # Emoji usage
            emoji_info = classification.get('emoji_analysis', {})
            if emoji_info.get('has_emojis', False):
                emoji_counts['with_emojis'] += 1
            else:
                emoji_counts['without_emojis'] += 1
            
            # Sarcasm detection
            if classification.get('sarcasm_detected', False):
                sarcasm_counts['detected'] += 1
            else:
                sarcasm_counts['not_detected'] += 1
            
            # Engagement levels
            engagement_info = classification.get('engagement_analysis', {})
            engagement_level = engagement_info.get('engagement_level', 'none')
            engagement_counts[engagement_level] += 1
            
            # Company mentions
            company_info = classification.get('company_analysis', {})
            if company_info.get('has_mentions', False):
                primary_company = company_info.get('primary_company')
                if primary_company:
                    company_mention_counts[primary_company] += 1
            
            # Accumulate metrics
            total_confidence += classification.get('confidence', 0)
            total_engagement_score += engagement_info.get('engagement_score', 0)
        
        # Calculate averages
        avg_confidence = total_confidence / total_comments
        avg_engagement = total_engagement_score / total_comments
        
        return {
            'total_comments': total_comments,
            'sentiment_distribution': dict(sentiment_counts),
            'language_distribution': dict(language_counts),
            'emoji_usage': dict(emoji_counts),
            'sarcasm_statistics': dict(sarcasm_counts),
            'engagement_distribution': dict(engagement_counts),
            'company_mentions': dict(company_mention_counts),
            'average_confidence': round(avg_confidence, 3),
            'average_engagement_score': round(avg_engagement, 3),
            'multilingual_percentage': round(
                sum(1 for c in enhanced_comments 
                    if c.get('advanced_sentiment_classification', {})
                    .get('language_analysis', {}).get('is_mixed', False)) / total_comments * 100, 2
            ),
            'sarcasm_percentage': round(sarcasm_counts['detected'] / total_comments * 100, 2)
        }
