            amplification_factor = 1.5t
        elif engagement_level == 'high':t
            amplification_factor = 1.3work
        elif engagement_level == 'medium':ork
            amplification_factor = 1.1tart
        else:t
            amplification_factor = 1.0/work
        work
        return {
            'engagement_score': round(engagement_score, 3),
            'engagement_level': engagement_level,
            'amplification_factor': amplification_factor,
            'like_weight': round(like_weight, 3),
            'reply_weight': round(reply_weight, 3),any
            'share_weight': round(share_weight, 3)eless/bad
        }useless/bad

    def _apply_contextual_sentiment_analysis(self, text_lower: str, positive_score: float, negative_score: float, sentiment_words: list) -> tuple:buying
        """Apply contextual sentiment analysis for complex patterns"""rom mistakes
        import reesign
        
        # Pattern 1: "Recommend" context analysisntext dependent)
        if 'recommend' in text_lower:omplicated
            # Positive recommend contextscated
            if any(pattern in text_lower for pattern in ['dil se recommend', 'strongly recommend', 'definitely recommend', 'highly recommend']):
                positive_score += 1.5stakes
                sentiment_words.append({'word': 'contextual_positive_recommend', 'sentiment': 'positive', 'language': 'contextual'})i-English mix)
            # Negative recommend contextsindi-English mix)
            elif any(pattern in text_lower for pattern in ['dont recommend', 'do not recommend', 'never recommend', 'not recommend']):
                negative_score += 1.5
                sentiment_words.append({'word': 'contextual_negative_recommend', 'sentiment': 'negative', 'language': 'contextual'})
        problems
        # Pattern 2: "Good" with negation analysisle seating
        good_negation_patterns = [
            r'not\s+good', r'nahi\s+good', r'nhi\s+good',
            'faulty design': 'negative',  # faulty design
            'buying mistake': 'negative', # mistake in buying
            'regret buying': 'negative',  # regret the purchase
            'shouldnt buy': 'negative',   # shouldn't buy
            'should not buy': 'negative', # should not buy
            'avoid buying': 'negative',   # avoid purchasing
            'dont buy': 'negative',       # don't buy
            'don\'t buy': 'negative',     # don't buy (with apostrophe)
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
            # Latest user examples - specific patterns from new misclassifications
            'no one will buy': 'negative', # prediction that nobody will purchase
            'nobody will buy': 'negative', # prediction that nobody will purchase
            'third class': 'negative',    # very poor quality descriptor
            '3rd class': 'negative',      # very poor quality descriptor (numeric)
            'third class hai': 'negative', # it is third class (Hindi-English)
            'service third class': 'negative', # service is third class
            'service third class hai': 'negative', # service is third class
            'kwalitiy third class': 'negative', # quality third class (typo)
            'quality third class': 'negative', # quality third class
            'aur service third class': 'negative', # and service third class
            'ki kwalitiy': 'negative',    # whose quality (often in negative context)
            'kwalitiy aur service': 'negative', # quality and service (often negative)
            'these guys service': 'negative', # these guys' service (often negative)
            'the way these guys': 'negative', # the way these guys (often critical)
            'service in place': 'negative',  # service in place (often sarcastic/negative)
            'cmpany fraud': 'negative',   # company fraud (informal typing)
            # Positive Hindi informal patterns - Enhanced for better detection
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
            # Enhanced LOCAL DIALECT patterns for better sentiment detection
            'gajab he': 'positive',       # amazing/awesome (from user example 1)
            'gajab hai': 'positive',      # amazing/awesome 
            'गजब है': 'positive',         # amazing/awesome
            'gajab': 'positive',          # amazing/awesome
            'so good': 'positive',        # very positive (from user example 1)
            'bilkul problem nahi': 'positive', # absolutely no problem (from user example 1)
            'bilkul problem nahi he': 'positive', # absolutely no problem
            'bilkul problem nahi hai': 'positive', # absolutely no problem
            'बिल्कुल प्रॉब्लम नहीं': 'positive', # absolutely no problem
            'बिल्कुल प्रॉब्लम नहीं है': 'positive', # absolutely no problem
            'number one': 'positive',     # #1, best (from user example 2)
            'no. 1': 'positive',          # number one
            'no 1': 'positive',           # number one
            '#1': 'positive',             # hashtag number one
            'leading nicely': 'positive', # doing well, positive growth (from user example 3)
            'is leading': 'positive',     # showing leadership
            'future': 'positive',         # forward-looking, optimistic (from user example 3)
            'is the future': 'positive',  # very positive about future prospects
            'bhai': 'neutral',            # brother - just an address form, neutral
            'भाई': 'neutral',             # brother in Hindi
            'update ke baad': 'neutral',  # after update - factual statement
            'अपडेट के बाद': 'neutral',    # after update in Hindi
            # Contextual "dil se" patterns - positive contexts
            'dil se recommend': 'positive',    # heartfelt recommendation
            'dil se suggest': 'positive',      # heartfelt suggestion
            'dil se bolta hun': 'positive',    # speaking from heart (usually positive advice)
            'dil se kehta hun': 'positive',    # saying from heart (usually positive)
            'dil se pasand': 'positive',       # like from heart
            'dil se khush': 'positive',        # happy from heart
            'दिल से रेकमेंड': 'positive',      # heartfelt recommendation
            'दिल से सुझाव': 'positive',       # heartfelt suggestion
            # Contextual "dil se" patterns - negative contexts  
            'dil se mana': 'negative',         # heartfelt refusal/warning
            'dil se mana karta': 'negative',   # heartfelt refusal
            'dil se mat lo': 'negative',       # heartfelt warning not to take
            'dil se avoid': 'negative',        # heartfelt avoidance advice
            'dil se warning': 'negative',      # heartfelt warning
            'dil se bol raha': 'context_dependent', # depends on what follows
            'दिल से मना': 'negative',          # heartfelt refusal
            'दिल से चेतावनी': 'negative',       # heartfelt warning
            # Enhanced QUESTION PATTERNS for neutral inquiry detection (user example 4)
            'real he ya fake': 'neutral',      # asking if real or fake - neutral inquiry
            'real hai ya fake': 'neutral',     # asking if real or fake
            'रियल है या फेक': 'neutral',       # asking if real or fake in Hindi
            'case aya he': 'neutral',          # case has come/happened - factual
            'case aya hai': 'neutral',         # case has come/happened - factual
            'केस आया है': 'neutral',           # case has come in Hindi
            'fire case': 'neutral',           # fire incident - factual reference
            'फायर केस': 'neutral',            # fire case in Hindi
            'ka fire case': 'neutral',        # [brand]'s fire case - factual inquiry
            'का फायर केस': 'neutral',         # [brand]'s fire case in Hindi
            'he ya': 'neutral',               # is it or - question pattern
            'hai ya': 'neutral',              # is it or - question pattern
            'है या': 'neutral',                # is it or in Hindi
            'he real': 'neutral',             # is real - question pattern
            'hai real': 'neutral',            # is real - question pattern
            'है रियल': 'neutral',             # is real in Hindi
            'ya fake': 'neutral',             # or fake - question ending
            'या फेक': 'neutral',              # or fake in Hindi
            'question mark context': 'neutral', # questions are generally neutral inquiries
            # Enhanced patterns for confused/questioning context (user example 3)
            'matlab matlab': 'neutral',       # what does this mean - confusion/inquiry
            'मतलब मतलब': 'neutral',           # what does this mean in Hindi
            'matlab': 'neutral',              # meaning/what - often questioning
            'मतलब': 'neutral',                # meaning in Hindi
            'kya matlab': 'neutral',          # what meaning - questioning
            'क्या मतलब': 'neutral',           # what meaning in Hindi
            'matlab kya': 'neutral',          # meaning what - questioning
            'मतलब क्या': 'neutral',           # meaning what in Hindi
            # Enhanced patterns from user examples for better accuracy
            'best hai': 'positive',           # is best - clearly positive (example 1)
            'i ride': 'neutral',              # factual statement about usage
            'km': 'neutral',                  # distance measurement - factual
            'ride km': 'neutral',             # distance covered - factual
            'have left': 'negative',          # abandoned product - negative (example 2)
            'left my': 'negative',            # abandoned product - negative
            'too costly': 'negative',         # expensive complaint - negative
            'costly service': 'negative',     # expensive service complaint
            'costly spare parts': 'negative', # expensive parts complaint
            'feku': 'negative',               # fake/liar - negative (example 3)
            'feku company': 'negative',       # fake company - negative
            'rone ka man': 'negative',        # want to cry - negative (example 4)
            'rone ka man kare': 'negative',   # feel like crying - negative
            'kharidne se pahle': 'neutral',   # before buying - advice context
            'service centre mein': 'neutral', # at service center - factual
            'jaaiye': 'neutral',              # go/visit - instruction
            'taklif dekhiae': 'negative',     # see the troubles - negative
            'no service centre': 'negative',  # lack of service - negative (example 5)
            'no responsibility': 'negative',  # no accountability - negative
            'no mileage garantee': 'negative',# no guarantee - negative
            'drop battery': 'negative',       # battery performance drop - negative
            'spare parts high costly': 'negative', # expensive spare parts
            'no skill workers': 'negative',   # unskilled staff - negative
            'no charging stations': 'negative', # lack of infrastructure - negative
            
            # Neutral inquiry and information seeking patterns
            'i am interested to know': 'neutral', # information seeking
            'interested to know': 'neutral',     # information seeking
            'want to know': 'neutral',           # information seeking
            'information about': 'neutral',      # seeking information
            'try to give': 'neutral',            # request for information
            'give sales number': 'neutral',      # specific data request
            'sales number': 'neutral',           # data inquiry
            'sales data': 'neutral',             # data inquiry
            'sales figure': 'neutral',           # data inquiry
            'sales info': 'neutral',             # data inquiry
            'which one is best': 'neutral',      # comparison request
            'which is better': 'neutral',        # comparison request
            'which one better': 'neutral',       # comparison request
            'your opinion': 'neutral',           # opinion request
            'opinion plz': 'neutral',            # opinion request (informal)
            'opinion please': 'neutral',         # opinion request
            'plzzz rply': 'neutral',             # reply request (informal)
            'please reply': 'neutral',           # reply request
            'pls reply': 'neutral',              # reply request (informal)
            'rply': 'neutral',                   # reply request (very informal)
            'give opinion': 'neutral',           # opinion request
            'suggest me': 'neutral',             # suggestion request
            'suggestion': 'neutral',             # suggestion request
            'advise me': 'neutral',              # advice request
            'advice': 'neutral',                 # advice request
            'comparison': 'neutral',             # comparison context
            'compare': 'neutral',                # comparison request
            'vs': 'neutral',                     # versus - comparison
            'between': 'neutral',                # comparison context
            'range of 11 to 20': 'neutral',     # data range specification
            'number range': 'neutral',           # data range context
            'lesser known companies': 'neutral', # factual description
            'nothing new': 'neutral',            # factual observation
            'everywhere': 'neutral',             # factual observation
            'information': 'neutral',            # information context
            'broo': 'neutral',                   # informal address (bro)
            'bro': 'neutral',                    # informal address
            'premium 2024': 'neutral',           # model specification
        }
        
        # Check for neutral inquiry patterns first (for user examples 3 & 4)
        has_neutral_inquiry = False
        neutral_inquiry_patterns = [
            'real he ya fake', 'real hai ya fake', 'रियल है या फेक',
            'he ya', 'hai ya', 'है या', 'ya fake', 'या फेक',
            'case aya he', 'case aya hai', 'केस आया है',
            'fire case', 'फायर केस',
            'matlab matlab', 'मतलब मतलब', 'matlab', 'मतलब',
            'kya matlab', 'क्या मतलब', 'matlab kya', 'मतलब क्या',
            # New patterns for information seeking and comparison requests
            'i am interested to know', 'interested to know', 'want to know',
            'information about', 'try to give', 'give sales number',
            'which one is best', 'which is better', 'which one better',
            'your opinion', 'opinion plz', 'opinion please', 'plzzz rply',
            'please reply', 'pls reply', 'rply', 'give opinion',
            'suggest me', 'suggestion', 'advise me', 'advice',
            'comparison', 'compare', 'vs', ' or ', 'between',  # Changed 'or' to ' or ' with spaces
            'sales number', 'sales data', 'sales figure', 'sales info',
            'range of 11 to 20', 'number range', 'lesser known companies',
            'nothing new', 'everywhere', 'information'
        ]
        
        # Check for pricing/factual information patterns (should be neutral)
        pricing_patterns = [
            'final price', 'price', 'cost', 'rupees', 'rs', '₹',
            'after subsidy', 'subsidy', 'accessories', 'etc',
            'v1 pro', 'model', 'variant', 'specification'
        ]
        
        # Check if text is primarily pricing/factual information
        is_pricing_info = (
            sum(1 for pattern in pricing_patterns if pattern in text_lower) >= 2 and
            len(text.split()) <= 15  # Short factual statements
        )
        
        for pattern in neutral_inquiry_patterns:
            if pattern in text_lower:
                has_neutral_inquiry = True
                break
                
        # Override with pricing context if detected
        if is_pricing_info:
            has_neutral_inquiry = True
        
        # Apply transliteration corrections first with contextual analysis
        for word, sentiment in transliteration_corrections.items():
            if word in text_lower:
                # Handle context-dependent patterns
                if sentiment == 'context_dependent':
                    if word == 'dil se bol raha':
                        # Check what follows "dil se bol raha"
                        if any(neg_word in text_lower for neg_word in ['mat', 'mana', 'avoid', 'warning', 'beware', 'dont', 'nahi']):
                            negative_score += 1.5
                            sentiment_words.append({'word': word, 'sentiment': 'negative', 'language': 'transliteration_contextual'})
                        elif any(pos_word in text_lower for pos_word in ['recommend', 'suggest', 'achha', 'good', 'badhiya', 'mast']):
                            positive_score += 2.0
                            sentiment_words.append({'word': word, 'sentiment': 'positive', 'language': 'transliteration_contextual'})
                        # If neutral context, treat as neutral - no score change
                elif sentiment == 'neutral':
                    # For neutral patterns, add to words but don't change scores
                    sentiment_words.append({'word': word, 'sentiment': 'neutral', 'language': 'transliteration'})
                elif sentiment == 'positive':
                    positive_score += 2.0  # Increased weight for positive informal patterns
                    sentiment_words.append({'word': word, 'sentiment': 'positive', 'language': 'transliteration'})
                else:  # negative
                    negative_score += 1
                    sentiment_words.append({'word': word, 'sentiment': 'negative', 'language': 'transliteration'})
        
        # Additional contextual analysis for complex patterns
        positive_score, negative_score = self._apply_contextual_sentiment_analysis(text_lower, positive_score, negative_score, sentiment_words)
        
        # Analyze English patterns with word boundary checks
        # Process English patterns for English, mixed, or unknown languages (fallback)
        if (language_info['primary_language'] in ['english', 'unknown'] or 
            'english' in language_info['languages'] or 
            language_info['is_mixed']):
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
        
        # Calculate final sentiment with advice request and neutral inquiry consideration
        total_score = positive_score + negative_score
        
        # Neutral inquiry patterns override other sentiment for factual questions (user example 4)
        # This should override even strong negative words when it's clearly a question
        if has_neutral_inquiry:
            sentiment = 'neutral'
            confidence = 0.85  # High confidence for neutral inquiries
        # First check for strong positive recommendations (should be positive)
        elif has_strong_positive_recommendation:
            sentiment = 'positive'
            if positive_score > 0:
                confidence = min(0.9, 0.6 + positive_score / max(total_score, 1) * 0.3)
            else:
                confidence = 0.8  # High confidence for strong recommendations even without other positive words
        # Strong negative or negative phrases override everything (except neutral inquiries and strong positive recommendations)
        elif (has_strong_negative or has_negative_phrase) and not is_advice_seeking:
            # Even if no negative words detected, negative phrases should make it negative
            if negative_score == 0 and (has_strong_negative or has_negative_phrase):
                negative_score = 3.0  # Strong negative assignment for phrase patterns
                total_score = positive_score + negative_score
            elif negative_score > 0:
                negative_score += 2.0  # Boost existing negative score
                total_score = positive_score + negative_score
            sentiment = 'negative'
            confidence = min(0.95, 0.8 + (negative_score / max(total_score, 1)) * 0.15)
        elif (has_strong_negative or has_negative_phrase) and is_advice_seeking:
            # Even advice seeking with strong negative should be negative
            if negative_score == 0:
                negative_score = 2.5
                total_score = positive_score + negative_score
            elif negative_score > 0:
                negative_score += 1.5
                total_score = positive_score + negative_score
            sentiment = 'negative'
            confidence = min(0.9, 0.7 + (negative_score / max(total_score, 1)) * 0.2)
        elif is_advice_seeking and not has_strong_negative and not has_negative_phrase:
            # For advice seeking, bias towards neutral unless strong sentiment
            # Advice-seeking should be neutral even with some positive words like "badhiya"
            # Only override if there are strong sentiment indicators or recommendations
            if total_score == 0:
                sentiment = 'neutral'
                confidence = 0.7  # High confidence for advice seeking
            elif has_strong_positive_recommendation or positive_score >= 3.0:  # Much higher threshold for advice seeking
                sentiment = 'positive'
                confidence = min(0.9, 0.5 + (positive_score - negative_score) / total_score * 0.3)
            elif negative_score > positive_score:
                sentiment = 'negative'
                confidence = min(0.9, 0.5 + (negative_score - positive_score) / total_score * 0.3)
            else:
                # Default to neutral for advice seeking even with some positive words
                sentiment = 'neutral'
                confidence = 0.75  # High confidence for neutral advice seeking
        elif is_advice_giving and (positive_score > 0 or negative_score > 0):
            # Advice giving should retain sentiment, but respect strong negative patterns
            if has_strong_negative or has_negative_phrase:
                sentiment = 'negative'
                confidence = min(0.9, 0.7 + (negative_score / max(total_score, 1)) * 0.2)
            elif negative_score > positive_score:
                sentiment = 'negative'
                confidence = min(0.9, 0.6 + (negative_score - positive_score) / total_score * 0.3)
            else:
                sentiment = 'positive'
                confidence = min(0.9, 0.5 + (positive_score - negative_score) / total_score * 0.4)
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
            'is_advice_seeking': is_advice_seeking,
            'is_advice_giving': is_advice_giving,
            'has_strong_positive_recommendation': has_strong_positive_recommendation,
            'has_strong_negative': has_strong_negative,
            'has_negative_phrase': has_negative_phrase,
            'text': text  # Add text for contextual analysis
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
        
        # Company mention relevance and contextual filtering
        contextual_override = False
        if target_oem:
            text_lower = pattern_sentiment.get('text', '').lower()
            
            # Check for irrelevant product mentions (e.g., petrol for electric OEMs)
            irrelevant_keywords = ['petrol', 'petrol scooter', 'gasoline', 'fuel', 'gas scooter', 'ic engine']
            has_irrelevant_product = any(keyword in text_lower for keyword in irrelevant_keywords)
            
            if company_info['has_mentions']:
                if target_oem in company_info['all_mentions']:
                    # This comment is about the target company - boost relevance
                    relevance_boost = company_info['all_mentions'][target_oem]['confidence'] * 0.2
                    base_confidence += relevance_boost
                    factors.append(f"target_company_relevance: +{relevance_boost:.2f}")
                elif company_info['primary_company'] and company_info['primary_company'] != target_oem:
                    # This comment is primarily about a competitor - neutralize sentiment
                    if base_sentiment in ['positive', 'negative']:
                        final_sentiment = 'neutral'
                        base_confidence = 0.85  # High confidence in neutralization
                        contextual_override = True
                        factors.append(f"competitor_sentiment_neutralized: {company_info['primary_company']} mentioned, not {target_oem}")
            elif has_irrelevant_product and base_sentiment in ['positive', 'negative']:
                # Positive/negative sentiment about irrelevant products (e.g., petrol praise for electric OEM)
                final_sentiment = 'neutral' 
                base_confidence = 0.85  # High confidence in neutralization
                contextual_override = True
                factors.append("irrelevant_product_neutralized: petrol/fuel mentioned for electric OEM")
            elif not company_info['has_mentions'] and base_sentiment in ['positive', 'negative']:
                # Generic sentiment without company mention - reduce confidence significantly
                base_confidence *= 0.5
                factors.append("generic_sentiment: no company mention, confidence reduced")
        else:
            # No target OEM specified - apply general logic
            if company_info['has_mentions'] and company_info['primary_company']:
                relevance_boost = 0.1
                base_confidence += relevance_boost
                factors.append(f"company_mentioned: +{relevance_boost:.2f}")
        
        # Skip emoji/score calculation if contextual override is applied
        if contextual_override:
            final_confidence = max(0.3, min(0.95, base_confidence))
            return {
                'sentiment': final_sentiment,
                'confidence': round(final_confidence, 3),
                'factors': factors,
                'final_score': 0.0,  # Neutral override
                'contextual_override': True
            }
        
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
