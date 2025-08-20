"""
Conversation Memory Service - Handles context and conversation history
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from collections import deque

class ConversationMemoryService:
    def __init__(self, max_history: int = 10, memory_file: str = "conversation_memory.json"):
        self.max_history = max_history
        self.memory_file = memory_file
        self.conversation_history = deque(maxlen=max_history)
        self.session_context = {}
        self.user_preferences = {}
        self.load_memory()
    
    def add_interaction(self, query: str, response: str, metadata: Dict[str, Any] = None):
        """Add a new interaction to conversation history"""
        interaction = {
            'timestamp': datetime.now().isoformat(),
            'query': query,
            'response': response,
            'metadata': metadata or {}
        }
        
        self.conversation_history.append(interaction)
        self._update_session_context(query, response, metadata)
        self.save_memory()
    
    def get_conversation_context(self, last_n: int = 5) -> str:
        """Get recent conversation context"""
        if not self.conversation_history:
            return ""
        
        recent_interactions = list(self.conversation_history)[-last_n:]
        
        context_parts = ["=== RECENT CONVERSATION CONTEXT ==="]
        
        for i, interaction in enumerate(recent_interactions, 1):
            timestamp = datetime.fromisoformat(interaction['timestamp'])
            time_str = timestamp.strftime("%Y-%m-%d %H:%M")
            
            context_parts.extend([
                f"\n--- Interaction {i} ({time_str}) ---",
                f"User: {interaction['query']}",
                f"Assistant: {interaction['response'][:200]}..." if len(interaction['response']) > 200 else f"Assistant: {interaction['response']}"
            ])
        
        # Add session context
        if self.session_context:
            context_parts.extend([
                "\n=== SESSION CONTEXT ===",
                f"Frequently discussed topics: {', '.join(self.session_context.get('topics', []))}",
                f"Preferred OEMs: {', '.join(self.session_context.get('preferred_oems', []))}",
                f"Analysis focus: {self.session_context.get('analysis_focus', 'General')}"
            ])
        
        context_parts.append("\n=== END CONTEXT ===\n")
        
        return '\n'.join(context_parts)
    
    def _update_session_context(self, query: str, response: str, metadata: Dict[str, Any]):
        """Update session context based on interaction"""
        # Extract topics from query
        topics = self._extract_topics(query)
        if topics:
            if 'topics' not in self.session_context:
                self.session_context['topics'] = []
            
            for topic in topics:
                if topic not in self.session_context['topics']:
                    self.session_context['topics'].append(topic)
            
            # Keep only last 10 topics
            self.session_context['topics'] = self.session_context['topics'][-10:]
        
        # Extract OEM preferences
        oems = self._extract_oems(query)
        if oems:
            if 'preferred_oems' not in self.session_context:
                self.session_context['preferred_oems'] = []
            
            for oem in oems:
                if oem not in self.session_context['preferred_oems']:
                    self.session_context['preferred_oems'].append(oem)
            
            # Keep only last 5 OEMs
            self.session_context['preferred_oems'] = self.session_context['preferred_oems'][-5:]
        
        # Update analysis focus
        analysis_types = self._extract_analysis_type(query)
        if analysis_types:
            self.session_context['analysis_focus'] = analysis_types[-1]
        
        # Track time-based queries
        time_periods = self._extract_time_references(query)
        if time_periods:
            self.session_context['time_focus'] = time_periods[-1]
    
    def _extract_topics(self, text: str) -> List[str]:
        """Extract discussion topics from text"""
        text_lower = text.lower()
        
        topic_keywords = {
            'service': ['service', 'support', 'maintenance', 'repair', 'center'],
            'battery': ['battery', 'range', 'charging', 'charge', 'power'],
            'performance': ['performance', 'speed', 'acceleration', 'power'],
            'price': ['price', 'cost', 'expensive', 'cheap', 'value', 'money'],
            'quality': ['quality', 'build', 'reliability', 'durable'],
            'comparison': ['compare', 'vs', 'versus', 'better', 'best'],
            'sentiment': ['sentiment', 'opinion', 'feedback', 'review'],
            'export': ['export', 'download', 'excel', 'word', 'report'],
            'temporal': ['month', 'year', 'quarter', 'time', 'period', 'trend']
        }
        
        topics = []
        for topic, keywords in topic_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                topics.append(topic)
        
        return topics
    
    def _extract_oems(self, text: str) -> List[str]:
        """Extract OEM names from text"""
        text_lower = text.lower()
        
        oem_patterns = {
            'Ola Electric': ['ola', 'ola electric'],
            'TVS iQube': ['tvs', 'iqube', 'tvs iqube'],
            'Bajaj Chetak': ['bajaj', 'chetak', 'bajaj chetak'],
            'Ather': ['ather'],
            'Hero Vida': ['hero', 'vida', 'hero vida']
        }
        
        found_oems = []
        for oem_name, patterns in oem_patterns.items():
            if any(pattern in text_lower for pattern in patterns):
                found_oems.append(oem_name)
        
        return found_oems
    
    def _extract_analysis_type(self, text: str) -> List[str]:
        """Extract type of analysis being requested"""
        text_lower = text.lower()
        
        analysis_types = []
        
        if any(word in text_lower for word in ['sentiment', 'feeling', 'opinion']):
            analysis_types.append('sentiment')
        
        if any(word in text_lower for word in ['compare', 'comparison', 'vs', 'versus']):
            analysis_types.append('comparison')
        
        if any(word in text_lower for word in ['trend', 'over time', 'temporal', 'month', 'year']):
            analysis_types.append('temporal')
        
        if any(word in text_lower for word in ['export', 'download', 'excel', 'report']):
            analysis_types.append('export')
        
        if any(word in text_lower for word in ['brand', 'strength', 'reputation']):
            analysis_types.append('brand_analysis')
        
        return analysis_types
    
    def _extract_time_references(self, text: str) -> List[str]:
        """Extract time period references from text"""
        import re
        
        text_lower = text.lower()
        time_refs = []
        
        # Month patterns
        months = ['january', 'february', 'march', 'april', 'may', 'june',
                 'july', 'august', 'september', 'october', 'november', 'december']
        
        for month in months:
            if month in text_lower:
                year_match = re.search(r'\b(20\d{2})\b', text)
                year = year_match.group(1) if year_match else str(datetime.now().year)
                time_refs.append(f"{month.title()} {year}")
        
        # Quarter patterns
        quarter_match = re.search(r'q[1-4]|quarter [1-4]', text_lower)
        if quarter_match:
            year_match = re.search(r'\b(20\d{2})\b', text)
            year = year_match.group(1) if year_match else str(datetime.now().year)
            time_refs.append(f"{quarter_match.group().upper()} {year}")
        
        # Year patterns
        year_match = re.search(r'\b(20\d{2})\b', text)
        if year_match and not any(month in text_lower for month in months):
            time_refs.append(f"Year {year_match.group(1)}")
        
        return time_refs
    
    def get_relevant_history(self, current_query: str, max_relevant: int = 3) -> List[Dict]:
        """Get conversation history relevant to current query"""
        if not self.conversation_history:
            return []
        
        current_topics = set(self._extract_topics(current_query))
        current_oems = set(self._extract_oems(current_query))
        current_analysis = set(self._extract_analysis_type(current_query))
        
        scored_interactions = []
        
        for interaction in self.conversation_history:
            past_topics = set(self._extract_topics(interaction['query']))
            past_oems = set(self._extract_oems(interaction['query']))
            past_analysis = set(self._extract_analysis_type(interaction['query']))
            
            # Calculate relevance score
            topic_overlap = len(current_topics.intersection(past_topics))
            oem_overlap = len(current_oems.intersection(past_oems))
            analysis_overlap = len(current_analysis.intersection(past_analysis))
            
            relevance_score = topic_overlap * 2 + oem_overlap * 3 + analysis_overlap * 2
            
            if relevance_score > 0:
                scored_interactions.append((relevance_score, interaction))
        
        # Sort by relevance and return top matches
        scored_interactions.sort(key=lambda x: x[0], reverse=True)
        
        return [interaction for _, interaction in scored_interactions[:max_relevant]]
    
    def get_user_preferences(self) -> Dict[str, Any]:
        """Get user preferences based on conversation history"""
        if not self.conversation_history:
            return {}
        
        # Analyze patterns in user queries
        oem_mentions = {}
        topic_frequencies = {}
        
        for interaction in self.conversation_history:
            # Count OEM mentions
            for oem in self._extract_oems(interaction['query']):
                oem_mentions[oem] = oem_mentions.get(oem, 0) + 1
            
            # Count topic frequencies
            for topic in self._extract_topics(interaction['query']):
                topic_frequencies[topic] = topic_frequencies.get(topic, 0) + 1
        
        # Determine preferences
        preferences = {
            'preferred_oems': sorted(oem_mentions.items(), key=lambda x: x[1], reverse=True)[:3],
            'frequent_topics': sorted(topic_frequencies.items(), key=lambda x: x[1], reverse=True)[:5],
            'session_length': len(self.conversation_history),
            'analysis_style': self.session_context.get('analysis_focus', 'general')
        }
        
        return preferences
    
    def clear_session(self):
        """Clear current session context but keep conversation history"""
        self.session_context = {}
    
    def save_memory(self):
        """Save conversation memory to file"""
        try:
            memory_data = {
                'conversation_history': list(self.conversation_history),
                'session_context': self.session_context,
                'user_preferences': self.user_preferences,
                'last_updated': datetime.now().isoformat()
            }
            
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(memory_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Failed to save conversation memory: {e}")
    
    def load_memory(self):
        """Load conversation memory from file"""
        if not os.path.exists(self.memory_file):
            return
        
        try:
            with open(self.memory_file, 'r', encoding='utf-8') as f:
                memory_data = json.load(f)
            
            # Load conversation history
            if 'conversation_history' in memory_data:
                for interaction in memory_data['conversation_history']:
                    self.conversation_history.append(interaction)
            
            # Load session context
            if 'session_context' in memory_data:
                self.session_context = memory_data['session_context']
            
            # Load user preferences
            if 'user_preferences' in memory_data:
                self.user_preferences = memory_data['user_preferences']
            
            print(f"✅ Loaded conversation memory: {len(self.conversation_history)} interactions")
            
        except Exception as e:
            print(f"⚠️ Failed to load conversation memory: {e}")
    
    def get_memory_summary(self) -> str:
        """Get a summary of conversation memory"""
        if not self.conversation_history:
            return "No conversation history available."
        
        preferences = self.get_user_preferences()
        
        summary_lines = [
            "=== CONVERSATION MEMORY SUMMARY ===",
            f"📝 Total Interactions: {len(self.conversation_history)}",
            f"🕒 Session Duration: {self._calculate_session_duration()}",
            ""
        ]
        
        if preferences.get('preferred_oems'):
            summary_lines.extend([
                "🏢 Most Discussed OEMs:",
                *[f"   • {oem}: {count} mentions" for oem, count in preferences['preferred_oems']],
                ""
            ])
        
        if preferences.get('frequent_topics'):
            summary_lines.extend([
                "💭 Frequent Topics:",
                *[f"   • {topic}: {count} times" for topic, count in preferences['frequent_topics']],
                ""
            ])
        
        if self.session_context:
            summary_lines.extend([
                "🎯 Current Session Focus:",
                f"   • Analysis Type: {self.session_context.get('analysis_focus', 'General')}",
                f"   • Time Focus: {self.session_context.get('time_focus', 'Current')}",
                ""
            ])
        
        return '\n'.join(summary_lines)
    
    def _calculate_session_duration(self) -> str:
        """Calculate duration of current session"""
        if len(self.conversation_history) < 2:
            return "Just started"
        
        first_interaction = datetime.fromisoformat(self.conversation_history[0]['timestamp'])
        last_interaction = datetime.fromisoformat(self.conversation_history[-1]['timestamp'])
        
        duration = last_interaction - first_interaction
        
        if duration.days > 0:
            return f"{duration.days} days"
        elif duration.seconds > 3600:
            hours = duration.seconds // 3600
            return f"{hours} hours"
        else:
            minutes = duration.seconds // 60
            return f"{minutes} minutes"
    
    def get_recent_for_llm(self, last_n: int = 10) -> List[Dict[str, str]]:
        """Return recent interactions formatted for LLM memory as a list of {'role': 'user'|'assistant', 'content': str}.

        This keeps the most recent N user/assistant pairs and is intended to be passed to LLM chat APIs
        so the model retains short-term conversational context.
        """
        if not self.conversation_history:
            return []

        recent = list(self.conversation_history)[-last_n:]
        messages: List[Dict[str, str]] = []
        for inter in recent:
            user_text = inter.get('query', '')
            assistant_text = inter.get('response', '')
            if user_text:
                messages.append({'role': 'user', 'content': user_text})
            if assistant_text:
                messages.append({'role': 'assistant', 'content': assistant_text})

        return messages
