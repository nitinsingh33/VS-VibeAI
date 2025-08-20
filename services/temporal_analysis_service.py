"""
Temporal Analysis Service - Enhanced with AI-powered sentiment analysis using Gemini 2.5 Pro
"""

import re
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dateutil import parser
from collections import defaultdict
import pandas as pd
import asyncio
import os

# Import the enhanced sentiment analyzer
from .enhanced_sentiment_analyzer import EnhancedSentimentAnalyzer

class TemporalAnalysisService:
    def __init__(self):
        """Initialize the temporal analysis service with enhanced sentiment analyzer"""
        self.enhanced_sentiment = EnhancedSentimentAnalyzer()
        print("✅ Temporal Analysis Service initialized with enhanced sentiment analyzer")
        
        self.month_patterns = {
            'january': 1, 'jan': 1,
            'february': 2, 'feb': 2,
            'march': 3, 'mar': 3,
            'april': 4, 'apr': 4,
            'may': 5,
            'june': 6, 'jun': 6,
            'july': 7, 'jul': 7,
            'august': 8, 'aug': 8,
            'september': 9, 'sep': 9, 'sept': 9,
            'october': 10, 'oct': 10,
            'november': 11, 'nov': 11,
            'december': 12, 'dec': 12
        }
        
        self.quarter_patterns = {
            'q1': [1, 2, 3], 'quarter 1': [1, 2, 3], 'first quarter': [1, 2, 3],
            'q2': [4, 5, 6], 'quarter 2': [4, 5, 6], 'second quarter': [4, 5, 6],
            'q3': [7, 8, 9], 'quarter 3': [7, 8, 9], 'third quarter': [7, 8, 9],
            'q4': [10, 11, 12], 'quarter 4': [10, 11, 12], 'fourth quarter': [10, 11, 12]
        }
        
    def _extract_product_mentions(self, comment: str) -> List[str]:
        """Extract product mentions and brands from comment"""
        
    def extract_time_period(self, query: str) -> Optional[Dict[str, Any]]:
        """Extract time period information from user query"""
        query_lower = query.lower()
        
        # Extract year
        year_match = re.search(r'\b(20\d{2})\b', query)
        year = int(year_match.group(1)) if year_match else datetime.now().year
        
        # Check for quarter patterns
        for quarter_key, months in self.quarter_patterns.items():
            if quarter_key in query_lower:
                return {
                    'type': 'quarter',
                    'year': year,
                    'months': months,
                    'description': f"{quarter_key.upper()} {year}",
                    'start_month': months[0],
                    'end_month': months[-1]
                }
        
        # Check for month patterns
        for month_name, month_num in self.month_patterns.items():
            if month_name in query_lower:
                # Check for specific date
                day_match = re.search(rf'\b(\d{{1,2}})\s+{month_name}', query_lower)
                if day_match:
                    day = int(day_match.group(1))
                    return {
                        'type': 'specific_date',
                        'year': year,
                        'month': month_num,
                        'day': day,
                        'description': f"{day} {month_name.title()} {year}"
                    }
                else:
                    return {
                        'type': 'month',
                        'year': year,
                        'month': month_num,
                        'description': f"{month_name.title()} {year}"
                    }
        
        # Check for year-only queries
        if year_match and not any(month in query_lower for month in self.month_patterns.keys()):
            return {
                'type': 'year',
                'year': year,
                'description': f"Year {year}"
            }
        
        # Check for duration patterns (last X months, past year, etc.)
        duration_patterns = [
            (r'last (\d+) months?', 'last_months'),
            (r'past (\d+) months?', 'last_months'),
            (r'previous (\d+) months?', 'last_months'),
            (r'last year', 'last_year'),
            (r'past year', 'last_year'),
            (r'last (\d+) years?', 'last_years')
        ]
        
        for pattern, duration_type in duration_patterns:
            match = re.search(pattern, query_lower)
            if match:
                if duration_type == 'last_months':
                    months_back = int(match.group(1))
                    end_date = datetime.now()
                    start_date = end_date - timedelta(days=months_back * 30)
                    return {
                        'type': 'duration',
                        'duration_type': 'months',
                        'value': months_back,
                        'start_date': start_date,
                        'end_date': end_date,
                        'description': f"Last {months_back} months"
                    }
                elif duration_type == 'last_year':
                    end_date = datetime.now()
                    start_date = end_date - timedelta(days=365)
                    return {
                        'type': 'duration',
                        'duration_type': 'year',
                        'value': 1,
                        'start_date': start_date,
                        'end_date': end_date,
                        'description': "Last year"
                    }
                elif duration_type == 'last_years':
                    years_back = int(match.group(1))
                    end_date = datetime.now()
                    start_date = end_date - timedelta(days=years_back * 365)
                    return {
                        'type': 'duration',
                        'duration_type': 'years',
                        'value': years_back,
                        'start_date': start_date,
                        'end_date': end_date,
                        'description': f"Last {years_back} years"
                    }
        
        return None
    
    def filter_comments_by_time_period(self, comments: List[Dict], time_period: Dict[str, Any]) -> List[Dict]:
        """Filter comments based on time period"""
        filtered_comments = []
        
        for comment in comments:
            comment_date = self._parse_comment_date(comment)
            if not comment_date:
                continue
                
            if self._is_comment_in_period(comment_date, time_period):
                filtered_comments.append(comment)
        
        return filtered_comments
    
    def _parse_comment_date(self, comment: Dict) -> Optional[datetime]:
        """Parse comment date from various formats"""
        date_str = comment.get('date', '')
        if not date_str:
            return None
            
        try:
            # Try parsing with dateutil (handles many formats)
            return parser.parse(date_str)
        except:
            try:
                # Try common formats
                formats = [
                    '%Y-%m-%d %H:%M:%S',
                    '%Y-%m-%d',
                    '%d/%m/%Y',
                    '%m/%d/%Y',
                    '%B %d, %Y',
                    '%d %B %Y'
                ]
                
                for fmt in formats:
                    try:
                        return datetime.strptime(date_str, fmt)
                    except:
                        continue
            except:
                pass
        
        return None
    
    def _is_comment_in_period(self, comment_date: datetime, time_period: Dict[str, Any]) -> bool:
        """Check if comment falls within the specified time period"""
        period_type = time_period['type']
        
        if period_type == 'month':
            return (comment_date.year == time_period['year'] and 
                   comment_date.month == time_period['month'])
        
        elif period_type == 'quarter':
            return (comment_date.year == time_period['year'] and 
                   comment_date.month in time_period['months'])
        
        elif period_type == 'year':
            return comment_date.year == time_period['year']
        
        elif period_type == 'specific_date':
            return (comment_date.year == time_period['year'] and 
                   comment_date.month == time_period['month'] and
                   comment_date.day == time_period['day'])
        
        elif period_type == 'duration':
            return (time_period['start_date'] <= comment_date <= time_period['end_date'])
        
        return False
    
    def analyze_sentiment_trends(self, comments_by_oem: Dict[str, List[Dict]], 
                                time_periods: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze sentiment trends across multiple time periods"""
        trends = {}
        
        for oem_name, comments in comments_by_oem.items():
            oem_trends = []
            
            for period in time_periods:
                period_comments = self.filter_comments_by_time_period(comments, period)
                sentiment_analysis = self._calculate_sentiment_metrics(period_comments)
                
                oem_trends.append({
                    'period': period['description'],
                    'comment_count': len(period_comments),
                    'sentiment_metrics': sentiment_analysis,
                    'period_info': period
                })
            
            trends[oem_name] = oem_trends
        
        return trends
    
    def _calculate_sentiment_metrics(self, comments: List[Dict]) -> Dict[str, Any]:
        """Calculate advanced sentiment metrics using AI analysis"""
        if not comments:
            return {
                'positive_count': 0,
                'negative_count': 0,
                'neutral_count': 0,
                'positive_percentage': 0.0,
                'negative_percentage': 0.0,
                'neutral_percentage': 0.0,
                'sentiment_score': 0.0,
                'total_comments': 0,
                'confidence_level': 0.0,
                'analysis_method': 'none'
            }
        
        # Use enhanced sentiment analyzer for all comment analysis
        return self._enhanced_sentiment_analysis(comments)
    
    def _enhanced_sentiment_analysis(self, comments: List[Dict]) -> Dict[str, Any]:
        """Enhanced sentiment analysis using the new sentiment analyzer"""
        try:
            total_comments = len(comments)
            if total_comments == 0:
                return {
                    'positive_count': 0,
                    'negative_count': 0,
                    'neutral_count': 0,
                    'positive_percentage': 0.0,
                    'negative_percentage': 0.0,
                    'neutral_percentage': 0.0,
                    'sentiment_score': 0.0,
                    'total_comments': 0,
                    'confidence_level': 0.0,
                    'analysis_method': 'enhanced',
                    'key_insights': 'No comments to analyze'
                }
            
            # Analyze each comment using enhanced sentiment analyzer
            sentiment_counts = {'positive': 0, 'negative': 0, 'neutral': 0}
            total_score = 0
            total_confidence = 0
            sarcasm_detected = 0
            multilingual_detected = 0
            
            for comment in comments:
                text = comment.get('text', '').strip()
                if not text:
                    continue
                    
                # Get enhanced sentiment analysis
                analysis = self.enhanced_sentiment.analyze_comment_sentiment(text)
                
                sentiment = analysis.get('sentiment', 'neutral')
                confidence = analysis.get('confidence', 0.5)
                score = analysis.get('sentiment_score', 0)
                
                # Count sentiments
                sentiment_counts[sentiment] += 1
                total_score += score
                total_confidence += confidence
                
                # Track special cases
                if analysis.get('sarcasm_detected', False):
                    sarcasm_detected += 1
                if analysis.get('is_multilingual', False):
                    multilingual_detected += 1
            
            # Calculate percentages
            positive_pct = (sentiment_counts['positive'] / total_comments) * 100
            negative_pct = (sentiment_counts['negative'] / total_comments) * 100
            neutral_pct = (sentiment_counts['neutral'] / total_comments) * 100
            
            # Average metrics
            avg_score = total_score / total_comments if total_comments > 0 else 0
            avg_confidence = total_confidence / total_comments if total_comments > 0 else 0
            
            # Generate insights
            insights = []
            if sarcasm_detected > 0:
                insights.append(f"{sarcasm_detected} comments with sarcasm detected")
            if multilingual_detected > 0:
                insights.append(f"{multilingual_detected} multilingual comments processed")
            
            dominant_sentiment = max(sentiment_counts, key=sentiment_counts.get)
            insights.append(f"Predominantly {dominant_sentiment} sentiment")
            
            return {
                'positive_count': sentiment_counts['positive'],
                'negative_count': sentiment_counts['negative'],
                'neutral_count': sentiment_counts['neutral'],
                'positive_percentage': round(positive_pct, 2),
                'negative_percentage': round(negative_pct, 2),
                'neutral_percentage': round(neutral_pct, 2),
                'sentiment_score': round(avg_score, 2),
                'total_comments': total_comments,
                'confidence_level': round(avg_confidence * 100, 1),
                'analysis_method': 'enhanced_ai',
                'key_insights': '; '.join(insights),
                'sarcasm_detected': sarcasm_detected,
                'multilingual_processed': multilingual_detected
            }
            
        except Exception as e:
            print(f'⚠️ Enhanced sentiment analysis failed: {e}, using fallback')
            return self._enhanced_keyword_sentiment_analysis(comments)
    
    def _enhanced_keyword_sentiment_analysis(self, comments: List[Dict]) -> Dict[str, Any]:
        """Enhanced keyword-based sentiment analysis with weights and context"""
        # Expanded and weighted keyword sets
        sentiment_keywords = {
            'highly_positive': {
                'keywords': ['excellent', 'outstanding', 'exceptional', 'brilliant', 'amazing', 'fantastic', 'perfect'],
                'weight': 3.0
            },
            'positive': {
                'keywords': ['good', 'great', 'nice', 'satisfied', 'happy', 'recommend', 'love', 'best', 'impressive'],
                'weight': 2.0
            },
            'mild_positive': {
                'keywords': ['okay', 'decent', 'fine', 'acceptable', 'reasonable', 'not bad'],
                'weight': 1.0
            },
            'highly_negative': {
                'keywords': ['terrible', 'awful', 'horrible', 'worst', 'pathetic', 'useless', 'disgusting'],
                'weight': -3.0
            },
            'negative': {
                'keywords': ['bad', 'poor', 'disappointed', 'hate', 'problem', 'issue', 'broken', 'defect'],
                'weight': -2.0
            },
            'mild_negative': {
                'keywords': ['could be better', 'not great', 'meh', 'average', 'so-so'],
                'weight': -1.0
            }
        }
        
        # Context modifiers
        negation_words = ['not', 'no', 'never', 'none', 'nothing', 'nowhere', 'nobody']
        intensifiers = ['very', 'really', 'extremely', 'totally', 'absolutely', 'completely']
        
        sentiment_scores = []
        sentiment_counts = {'positive': 0, 'negative': 0, 'neutral': 0}
        
        for comment in comments:
            text = comment.get('text', '').lower()
            if len(text.strip()) < 5:  # Skip very short comments
                continue
                
            comment_score = 0
            word_matches = 0
            
            # Analyze sentiment with weights and context
            words = text.split()
            for i, word in enumerate(words):
                for category, data in sentiment_keywords.items():
                    for keyword in data['keywords']:
                        if keyword in text:
                            weight = data['weight']
                            
                            # Check for negation (previous 2 words)
                            negated = any(neg in words[max(0, i-2):i] for neg in negation_words)
                            if negated:
                                weight *= -0.8  # Reverse but reduce intensity
                            
                            # Check for intensifiers
                            intensified = any(intens in words[max(0, i-1):i+2] for intens in intensifiers)
                            if intensified:
                                weight *= 1.5
                            
                            comment_score += weight
                            word_matches += 1
            
            # Normalize score based on comment length and matches
            if word_matches > 0:
                comment_score = comment_score / max(1, word_matches * 0.5)  # Avoid over-weighting
            
            sentiment_scores.append(comment_score)
            
            # Classify overall sentiment
            if comment_score > 0.5:
                sentiment_counts['positive'] += 1
            elif comment_score < -0.5:
                sentiment_counts['negative'] += 1
            else:
                sentiment_counts['neutral'] += 1
        
        total = len(comments)
        positive_pct = (sentiment_counts['positive'] / total) * 100
        negative_pct = (sentiment_counts['negative'] / total) * 100
        neutral_pct = (sentiment_counts['neutral'] / total) * 100
        
        # Calculate overall sentiment score with confidence adjustment
        overall_score = sum(sentiment_scores) / max(1, len(sentiment_scores)) * 20  # Scale to -100 to +100
        overall_score = max(-100, min(100, overall_score))  # Clamp to range
        
        # Calculate confidence based on score distribution
        if total > 50:
            confidence = min(95, 70 + (total - 50) * 0.3)  # Higher confidence with more data
        else:
            confidence = max(60, 40 + total)  # Lower confidence with less data
        
        return {
            'positive_count': sentiment_counts['positive'],
            'negative_count': sentiment_counts['negative'],
            'neutral_count': sentiment_counts['neutral'],
            'positive_percentage': round(positive_pct, 2),
            'negative_percentage': round(negative_pct, 2),
            'neutral_percentage': round(neutral_pct, 2),
            'sentiment_score': round(overall_score, 2),
            'total_comments': total,
            'confidence_level': round(confidence, 1),
            'analysis_method': 'enhanced_keywords'
        }
    
    def calculate_brand_strength(self, comments: List[Dict], competitors: List[str] = None) -> Dict[str, Any]:
        """Calculate advanced brand strength metrics with competitive analysis"""
        if not comments:
            return {
                'brand_strength_score': 0, 
                'metrics': {},
                'analysis_method': 'none',
                'confidence_level': 0.0
            }
        
        # Enhanced brand strength indicators with weights
        strength_indicators = {
            'loyalty': {
                'keywords': ['loyal', 'stick with', 'continue using', 'never switching', 'lifetime customer', 'brand advocate'],
                'weight': 4.0,
                'description': 'Customer loyalty and retention'
            },
            'recommendation': {
                'keywords': ['recommend', 'suggest', 'advise', 'should buy', 'must have', 'go for it'],
                'weight': 3.5,
                'description': 'Active recommendation behavior'
            },
            'quality_perception': {
                'keywords': ['quality', 'reliable', 'durable', 'well-built', 'solid', 'premium', 'top-notch'],
                'weight': 3.0,
                'description': 'Quality and reliability perception'
            },
            'satisfaction': {
                'keywords': ['satisfied', 'happy', 'pleased', 'content', 'delighted', 'thrilled', 'love it'],
                'weight': 2.5,
                'description': 'Overall satisfaction levels'
            },
            'performance': {
                'keywords': ['fast', 'quick', 'efficient', 'powerful', 'smooth', 'responsive', 'excellent performance'],
                'weight': 2.5,
                'description': 'Performance appreciation'
            },
            'value_perception': {
                'keywords': ['worth it', 'value for money', 'good deal', 'affordable', 'best price', 'cost-effective'],
                'weight': 2.0,
                'description': 'Value for money perception'
            },
            'innovation': {
                'keywords': ['innovative', 'advanced', 'cutting-edge', 'modern', 'futuristic', 'technology'],
                'weight': 2.0,
                'description': 'Innovation and technology perception'
            }
        }
        
        weakness_indicators = {
            'service_issues': {
                'keywords': ['service center', 'poor service', 'service problem', 'maintenance issue', 'repair delay'],
                'weight': -3.5,
                'description': 'Service and support issues'
            },
            'quality_issues': {
                'keywords': ['defect', 'broken', 'faulty', 'poor quality', 'manufacturing defect', 'build quality'],
                'weight': -3.0,
                'description': 'Quality and reliability problems'
            },
            'defection': {
                'keywords': ['switching', 'changing to', 'moving to', 'left for', 'buying competitor', 'never again'],
                'weight': -4.0,
                'description': 'Customer defection indicators'
            },
            'dissatisfaction': {
                'keywords': ['disappointed', 'unsatisfied', 'regret', 'waste of money', 'worst decision', 'hate'],
                'weight': -2.5,
                'description': 'General dissatisfaction'
            },
            'performance_issues': {
                'keywords': ['slow', 'poor performance', 'not working', 'failed', 'disappointing speed', 'laggy'],
                'weight': -2.0,
                'description': 'Performance-related complaints'
            }
        }
        
        # Calculate weighted scores
        strength_metrics = {}
        weakness_metrics = {}
        total_strength_score = 0
        total_weakness_score = 0
        
        for comment in comments:
            text = comment.get('text', '').lower()
            comment_length = len(text.split())
            
            # Calculate strength scores with normalization
            for category, data in strength_indicators.items():
                matches = sum(1 for keyword in data['keywords'] if keyword in text)
                if matches > 0:
                    # Normalize by comment length to avoid bias toward longer comments
                    normalized_score = (matches * data['weight']) / max(1, comment_length / 10)
                    if category not in strength_metrics:
                        strength_metrics[category] = {'count': 0, 'score': 0, 'weight': data['weight']}
                    strength_metrics[category]['count'] += matches
                    strength_metrics[category]['score'] += normalized_score
                    total_strength_score += normalized_score
            
            # Calculate weakness scores
            for category, data in weakness_indicators.items():
                matches = sum(1 for keyword in data['keywords'] if keyword in text)
                if matches > 0:
                    normalized_score = (matches * abs(data['weight'])) / max(1, comment_length / 10)
                    if category not in weakness_metrics:
                        weakness_metrics[category] = {'count': 0, 'score': 0, 'weight': data['weight']}
                    weakness_metrics[category]['count'] += matches
                    weakness_metrics[category]['score'] += normalized_score
                    total_weakness_score += normalized_score
        
        total_comments = len(comments)
        
        # Calculate brand strength score (0-100) with advanced weighting
        if total_comments > 0:
            strength_density = total_strength_score / total_comments
            weakness_density = total_weakness_score / total_comments
            
            # Apply sigmoid function for better distribution
            import math
            raw_score = strength_density - weakness_density
            brand_strength_score = 50 + (40 * math.tanh(raw_score / 2))  # Sigmoid scaling
            brand_strength_score = max(0, min(100, brand_strength_score))
        else:
            brand_strength_score = 50  # Neutral
        
        # Calculate competitive positioning if competitors provided
        competitive_analysis = {}
        if competitors:
            competitor_mentions = defaultdict(int)
            for comment in comments:
                text = comment.get('text', '').lower()
                for competitor in competitors:
                    if competitor.lower() in text:
                        competitor_mentions[competitor] += 1
            
            competitive_analysis = {
                'competitor_mentions': dict(competitor_mentions),
                'brand_awareness_relative': len(competitor_mentions) > 0
            }
        
        # Calculate confidence based on data volume and signal strength
        signal_strength = (total_strength_score + total_weakness_score) / max(1, total_comments)
        if total_comments > 100:
            base_confidence = 90
        elif total_comments > 50:
            base_confidence = 80
        else:
            base_confidence = 60
        
        confidence_level = min(95, base_confidence + (signal_strength * 5))
        
        # Generate insights
        top_strengths = sorted(strength_metrics.items(), key=lambda x: x[1]['score'], reverse=True)[:3]
        top_weaknesses = sorted(weakness_metrics.items(), key=lambda x: x[1]['score'], reverse=True)[:3]
        
        return {
            'brand_strength_score': round(brand_strength_score, 2),
            'confidence_level': round(confidence_level, 1),
            'analysis_method': 'advanced_weighted',
            'total_comments_analyzed': total_comments,
            'strength_density': round(total_strength_score / total_comments, 3),
            'weakness_density': round(total_weakness_score / total_comments, 3),
            'top_strengths': [{'category': cat, 'score': data['score'], 'mentions': data['count']} 
                             for cat, data in top_strengths],
            'top_weaknesses': [{'category': cat, 'score': data['score'], 'mentions': data['count']} 
                              for cat, data in top_weaknesses],
            'competitive_analysis': competitive_analysis,
            'detailed_metrics': {
                'strength_categories': strength_metrics,
                'weakness_categories': weakness_metrics
            }
        }
    
    def generate_temporal_summary(self, temporal_analysis: Dict[str, Any], 
                                 time_period: Dict[str, Any]) -> str:
        """Generate a summary of temporal analysis results"""
        summary_lines = [
            f"=== TEMPORAL ANALYSIS FOR {time_period['description'].upper()} ===",
            ""
        ]
        
        if not temporal_analysis:
            summary_lines.append("No data available for the specified time period.")
            return '\n'.join(summary_lines)
        
        # Overall statistics
        total_comments = sum(
            sum(period['comment_count'] for period in oem_data) 
            if isinstance(oem_data, list) else 0
            for oem_data in temporal_analysis.values()
        )
        
        summary_lines.extend([
            f"📊 Total Comments Analyzed: {total_comments}",
            f"🏢 OEMs Covered: {len(temporal_analysis)}",
            ""
        ])
        
        # Per-OEM analysis
        for oem_name, oem_data in temporal_analysis.items():
            if isinstance(oem_data, list) and oem_data:
                latest_period = oem_data[-1]  # Most recent period
                metrics = latest_period['sentiment_metrics']
                
                summary_lines.extend([
                    f"🔍 {oem_name}:",
                    f"   • Comments: {latest_period['comment_count']}",
                    f"   • Sentiment Score: {metrics['sentiment_score']}/100",
                    f"   • Positive: {metrics['positive_percentage']}%",
                    f"   • Negative: {metrics['negative_percentage']}%",
                    ""
                ])
        
        return '\n'.join(summary_lines)
