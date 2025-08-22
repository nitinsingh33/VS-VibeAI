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
            # Additional heart emoji variations
            '❤': 0.9, '🧡': 0.8, '💛': 0.8, '💚': 0.8, '💙': 0.8, '💜': 0.8,
            # Additional positive emojis
            '👑': 0.9, '🔥': 0.8, '⚡': 0.7, '💎': 0.8, '🌈': 0.7, '☀️': 0.7,
            
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
            # Decorative/functional emojis (neutral)
            '📌': 0.0, '📍': 0.0, '🔴': 0.0, '🟡': 0.0, '🟢': 0.0, '⚪': 0.0, '⚫': 0.0,
            
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
                'satisfied', 'happy', 'pleased', 'delighted', 'thrilled',
                # Enhanced positive patterns from user examples
                'best', 'best hai', 'ride', 'smooth', 'comfortable', 'reliable',
                'value for money', 'worth it', 'good mileage', 'efficient',
                'smooth ride', 'comfortable ride', 'nice performance', 'good pickup',
                'powerful', 'strong', 'durable', 'long lasting', 'excellent range',
                'fast charging', 'quick charging', 'good battery', 'excellent battery',
                'superior', 'top quality', 'premium', 'luxury', 'classy',
                'stylish', 'attractive', 'beautiful', 'gorgeous', 'stunning',
                # Market share and growth patterns
                'market share', 'badh raha', 'badh raha hai', 'बढ़ रहा', 'बढ़ रहा है',
                'increasing', 'growing', 'growth', 'expansion', 'rising', 'improve',
                'progress', 'success', 'successful', 'winning', 'dominating',
                # King/leadership and dominance patterns
                'king', 'king of', 'राजा', 'बादशाह', 'leader', 'leading', 'dominant',
                'champion', 'winner', 'number one', 'no 1', '#1', 'top brand'
            ],
            'hindi': [
                'अच्छा', 'बढ़िया', 'शानदार', 'उत्कृष्ट', 'बेहतरीन', 'जबरदस्त',
                'सुंदर', 'प्यारा', 'मस्त', 'धमाकेदार', 'कमाल', 'लाजवाब',
                # Enhanced Hindi positive patterns
                'बेस्ट', 'बेस्ट है', 'सबसे अच्छा', 'टॉप', 'नंबर वन',
                'फर्स्ट क्लास', 'बहुत बढ़िया', 'एकदम मस्त', 'गजब',
                'जोरदार', 'धाकड़', 'छप्पर फाड़', 'जानदार', 'बेमिसाल',
                'खुशी', 'संतुष्ट', 'खुश', 'प्रसन्न', 'आनंद',
                # Mixed language positive patterns
                'achha', 'badhiya', 'shandar', 'excellent', 'zabardast', 'mast',
                'best hai', 'ek number', 'first class', 'top class', 'superb hai',
                'bahut achha', 'bahut badhiya', 'ekdam mast', 'gajab', 'jordar'
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
                'warning', 'beware', 'avoid', 'dont buy', 'don\'t buy', 'do not buy', 'money waste',
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
                'डिजाइन अच्छा नही', 'design achha nahi', 'yamaha niken',
                # Enhanced negative patterns from user examples  
                'left', 'leave', 'left my', 'have left', 'too costly', 'very costly',
                'expensive', 'overpriced', 'costly service', 'costly spare parts',
                'high cost', 'costly parts', 'expensive parts', 'feku', 'fake company',
                'cry', 'crying', 'rone ka man', 'rona aa jaye', 'regret',
                'no service', 'no responsibility', 'no guarantee', 'no support',
                'no charging stations', 'no skill workers', 'unskilled', 'taklif',
                'takleef', 'problem', 'issues', 'troubles', 'difficulties',
                'drop', 'battery drop', 'range drop', 'mileage drop', 'performance drop',
                'spare parts high', 'parts costly', 'maintenance expensive',
                # Latest user examples - negative prediction and quality issues
                'no one will buy', 'nobody will buy', 'none will buy', 'no one buys',
                'third class', '3rd class', 'third grade', 'low class', 'bottom class',
                'kwalitiy', 'kuality', 'qualitiy', 'qualty', 'kwality', # quality misspellings
                'service third class', 'third class service', 'third class hai',
                'the way these guys', 'these guys service', 'service in place'
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
                'chور', 'chor', 'चोर कंपनी', 'chor company', 'चोर कम्पनी',
                # Enhanced Hindi negative patterns from user examples
                'छोड़ दिया', 'छोड़ा', 'leave कर दिया', 'बहुत महंगा', 'ज्यादा महंगा',
                'महंगी सर्विस', 'महंगे पार्ट्स', 'फेकू', 'फेक कंपनी', 'झूठी कंपनी',
                'रोने का मन', 'रोना आ जाए', 'पछतावा', 'अफसोस', 'गलती',
                'कोई सर्विस नहीं', 'जिम्मेदारी नहीं', 'गारंटी नहीं', 'सपोर्ट नहीं',
                'चार्जिंग स्टेशन नहीं', 'स्किल वर्कर नहीं', 'तकलीफ', 'परेशानी',
                'ड्रॉप', 'बैटरी ड्रॉप', 'रेंज कम', 'माइलेज कम', 'परफॉर्मेंस खराब',
                'स्पेयर पार्ट्स महंगे', 'पार्ट्स कॉस्टली', 'मेंटेनेंस महंगा',
                # Additional Hindi negative advice patterns  
                'मत लेना', 'mat lena', 'मत लो', 'mat lo', 'नहीं लेना', 'nahi lena',
                'avoid karo', 'बचना', 'bachna', 'मत खरीदो', 'mat kharido'
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

    def _apply_contextual_sentiment_analysis(self, text_lower: str, positive_score: float, negative_score: float, sentiment_words: list) -> tuple:
        """Apply contextual sentiment analysis for complex patterns"""
        import re
        
        # Pattern 1: "Recommend" context analysis
        if 'recommend' in text_lower:
            # Positive recommend contexts
            if any(pattern in text_lower for pattern in ['dil se recommend', 'strongly recommend', 'definitely recommend', 'highly recommend']):
                positive_score += 1.5
                sentiment_words.append({'word': 'contextual_positive_recommend', 'sentiment': 'positive', 'language': 'contextual'})
            # Negative recommend contexts
            elif any(pattern in text_lower for pattern in ['dont recommend', 'do not recommend', 'never recommend', 'not recommend']):
                negative_score += 1.5
                sentiment_words.append({'word': 'contextual_negative_recommend', 'sentiment': 'negative', 'language': 'contextual'})
        
        # Pattern 2: "Good" with negation analysis
        good_negation_patterns = [
            r'not\s+good', r'nahi\s+good', r'nhi\s+good',
            r'good\s+nahi', r'good\s+nhi', r'achha\s+nahi', r'achha\s+nhi'
        ]
        for pattern in good_negation_patterns:
            if re.search(pattern, text_lower):
                negative_score += 1.5
                sentiment_words.append({'word': f'negated_good_{pattern}', 'sentiment': 'negative', 'language': 'contextual'})
        
        # Pattern 3: "Dil se" context beyond direct patterns
        if 'dil se' in text_lower and 'dil se recommend' not in text_lower and 'dil se mana' not in text_lower:
            # Check broader context
            context_window = text_lower
            # Look for negative context indicators
            negative_indicators = ['mat', 'mana', 'avoid', 'warning', 'beware', 'dont', 'nahi', 'problem', 'issue']
            positive_indicators = ['suggest', 'achha', 'good', 'badhiya', 'mast', 'best', 'love', 'like']
            
            neg_count = sum(1 for indicator in negative_indicators if indicator in context_window)
            pos_count = sum(1 for indicator in positive_indicators if indicator in context_window)
            
            if neg_count > pos_count:
                negative_score += 1.0
                sentiment_words.append({'word': 'dil_se_negative_context', 'sentiment': 'negative', 'language': 'contextual'})
            elif pos_count > neg_count:
                positive_score += 1.0
                sentiment_words.append({'word': 'dil_se_positive_context', 'sentiment': 'positive', 'language': 'contextual'})
        
        # Pattern 4: Sarcastic positive patterns
        sarcastic_patterns = [
            r'(great|excellent|amazing)\s+(service|experience)\s+.*(problem|issue|terrible)',
            r'(love|loved)\s+.*(service\s+center|repair|multiple\s+times)',
            r'(perfect|fantastic)\s+.*(again|third\s+time|fourth\s+time)'
        ]
        for pattern in sarcastic_patterns:
            if re.search(pattern, text_lower):
                negative_score += 2.0  # Strong negative for sarcasm
                sentiment_words.append({'word': f'sarcastic_pattern_{pattern[:20]}', 'sentiment': 'negative', 'language': 'contextual'})
        
        return positive_score, negative_score

    def analyze_sentiment_patterns(self, text: str, language_info: Dict) -> Dict[str, Any]:
        """Analyze sentiment using pattern matching with improved word boundary detection"""
        import re  # Import re module for regex operations
        
        text_lower = text.lower()
        
        positive_score = 0
        negative_score = 0
        sentiment_words = []
        
        # Analyze emojis and integrate into sentiment scoring
        emoji_info = self.analyze_emojis(text)
        if emoji_info['has_emojis']:
            emoji_score = emoji_info['emoji_sentiment_score']
            
            # Check for context-less emoji patterns (just emojis with minimal text)
            text_without_emojis = self.emoji_regex.sub('', text).strip()
            words_without_emojis = [w for w in text_without_emojis.split() if len(w) > 2]
            
            # If text is mostly emojis or very short, treat as neutral
            is_context_less = (
                len(text_without_emojis) <= 3 or  # Very short text
                len(words_without_emojis) <= 1 or  # Only 1 meaningful word
                text_without_emojis.lower() in ['hi', 'hello', 'hey', 'हाय', 'हैलो'] or  # Simple greetings
                all(len(w) <= 3 for w in words_without_emojis)  # Only very short words
            )
            
            if is_context_less:
                # Don't add emoji score for context-less emojis
                pass  
            else:
                # Convert emoji score to positive/negative scores for meaningful context
                if emoji_score > 0:
                    positive_score += emoji_score * 2.0  # Amplify emoji influence
                    sentiment_words.append({'word': f"emojis({emoji_info['emoji_count']})", 'sentiment': 'positive', 'language': 'emoji'})
                elif emoji_score < 0:
                    negative_score += abs(emoji_score) * 2.0  # Amplify emoji influence
                    sentiment_words.append({'word': f"emojis({emoji_info['emoji_count']})", 'sentiment': 'negative', 'language': 'emoji'})
        
        # Check for advice SEEKING patterns (should be neutral)
        # Distinguish from advice GIVING which should retain sentiment
        advice_seeking_patterns = [
            'suggest me', 'recommend me', 'advice me', 'help me choose', 'bta do', 'batao mujhe', 'tell me which',
            'please help', 'mujhe chahiye', 'kharidna hai', 'buy karna hai', 'purchase karna hai', 'planning to buy',
            'bhaiya suggest', 'sir please', 'confusion hai', 'decide nahi kar pa', 'choice kya karu', 'option batao', 'budget me kya',
            'suggestion chahiye', 'guide karo', 'kya lena chahiye', 'dijiye suggestion', 'bataye please', 'should i buy',
            'which one to buy', 'what to buy', 'help me choose', 'suggest karo please', 'advice dena',
            # Additional patterns from user examples
            'suggest kar dijiye', 'kaunsi electric scooty', 'leni chahiye', 'please bhaiya bta dijiye',
            'mere liye koi badhiya', 'mera range', 'mujhe facility nhi chahiye', 'battery backup acha hona chahiye',
            'range km se km', 'digital metre', 'charging station', 'mile toh bhi chalega',
            'ghar me lakar charge kar lunga', 'nearby ka showroom hai'
        ]
        
        # Advice GIVING patterns (should retain sentiment)
        advice_giving_patterns = [
            'recommend karta hu', 'suggest karta hu', 'advice deta hu', 'kehta hu',
            'mai recommend', 'mai suggest', 'mera suggestion', 'meri advice',
            'sabko kehta hu', 'sabko bolta hu', 'everyone ko', 'sab log'
        ]
        
        # Check for strong positive recommendation patterns
        strong_positive_recommendation_patterns = [
            'hi lena', 'yehi lena', 'iske hi lena', 'bas yehi', 'sirf yehi',
            'only this', 'bas yahi', 'definitely lena', 'zaroor lena'
        ]
        
        # Strong negative patterns that should override neutral bias
        strong_negative_patterns = [
            'fraud', 'dhokha', 'dhoka', 'cheat', 'cheating', 'scam', 'fake',
            'duplicate', 'copy', 'loot', 'looting', 'theft', 'stealing', 'chori',
            'thagi', 'beimani', 'ripping off', 'ripoff', 'disaster', 'nightmare',
            'worst company', 'pathetic service', 'useless service', 'terrible service',
            'never again', 'never buy', 'warning', 'beware', 'avoid', 'dont buy', 'don\'t buy',
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
            'kmpny froud', 'cmpany fraud', 'hero froud', 'ola froud', 'ather froud',
            # Additional patterns from user examples to improve accuracy
            'have left my', 'left my ola', 'too costly service', 'too costly spare',
            'costly spare parts', 'feku company', 'just like modi', 'rone ka man kare',
            'kharidne se pahle service centre', 'no service centre responsibility',
            'no mileage garantee', 'spare parts high costly', 'no skill workers',
            'no charging stations', 'taklif dekhiae', 'owners ka taklif',
            'battery drop', '42% to 36%', '36% to 1%', 'drop battery',
            'high costly', 'costly parts', 'expensive maintenance',
            # Latest user examples - strong negative predictions and quality issues
            'no one will buy', 'nobody will buy', 'none will buy', 'no one buys',
            'third class', '3rd class', 'third grade', 'low class', 'bottom class',
            'service third class', 'third class service', 'third class hai',
            'kwalitiy third class', 'quality third class', 'aur service third class'
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
            r'stay.*away.*from',
            # Additional patterns from user examples for better accuracy
            r'have.*left.*my',
            r'left.*my.*ola',
            r'too.*costly.*service',
            r'too.*costly.*spare',
            r'costly.*spare.*parts',
            r'feku.*company',
            r'just.*like.*modi',
            r'rone.*ka.*man.*kare',
            r'no.*service.*centre.*responsibility',
            r'no.*mileage.*garantee',
            r'spare.*parts.*high.*costly',
            r'no.*skill.*workers',
            r'no.*charging.*stations',
            r'owners.*ka.*taklif',
            r'battery.*drop',
            r'\d+%.*to.*\d+%.*drop',
            r'high.*costly.*parts',
            r'kharidne.*se.*pahle.*service.*centre',
            r'taklif.*dekhiae'
        ]
        
        # Check if this is advice seeking (neutral) vs advice giving (retain sentiment)
        is_advice_seeking = any(pattern in text_lower for pattern in advice_seeking_patterns)
        is_advice_giving = any(pattern in text_lower for pattern in advice_giving_patterns)
        has_strong_positive_recommendation = any(pattern in text_lower for pattern in strong_positive_recommendation_patterns)
        
        # Check for strong negative patterns with word boundaries to avoid false matches
        has_strong_negative = False
        import re
        for pattern in strong_negative_patterns:
            # Use word boundary for single words, exact match for phrases
            if ' ' in pattern:  # Multi-word phrase
                if pattern in text_lower:
                    has_strong_negative = True
                    break
            else:  # Single word - use word boundary
                if re.search(r'\b' + re.escape(pattern) + r'\b', text_lower):
                    has_strong_negative = True
                    break
        
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
