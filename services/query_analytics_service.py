"""
Query Analytics Service - Tracks user queries and system performance
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
import uuid

@dataclass
class QueryLog:
    timestamp: str
    query_id: str
    user_query: str
    response_preview: str  # First 200 chars
    processing_time: float
    analysis_method: str
    confidence_level: Optional[float]
    total_comments: Optional[int]
    export_requested: bool
    user_ip: Optional[str]
    user_agent: Optional[str]
    session_id: Optional[str]
    response_length: int
    temporal_analysis_used: bool
    oems_mentioned: List[str]
    error_occurred: bool
    error_message: Optional[str]

class QueryAnalyticsService:
    def __init__(self):
        self.log_file = "query_analytics.json"
        self.session_file = "user_sessions.json"
        self.daily_stats_file = "daily_query_stats.json"
        
    def log_query(self, 
                  user_query: str,
                  response: str,
                  processing_time: float,
                  analysis_metadata: Dict[str, Any] = None,
                  user_info: Dict[str, Any] = None,
                  error_info: Dict[str, Any] = None) -> str:
        """Log a user query with comprehensive metadata"""
        
        query_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        
        # Extract metadata
        metadata = analysis_metadata or {}
        user_data = user_info or {}
        error_data = error_info or {}
        
        # Create query log entry
        query_log = QueryLog(
            timestamp=timestamp,
            query_id=query_id,
            user_query=user_query,
            response_preview=response[:200] + "..." if len(response) > 200 else response,
            processing_time=processing_time,
            analysis_method=metadata.get('analysis_method', 'unknown'),
            confidence_level=metadata.get('confidence_level'),
            total_comments=metadata.get('total_comments'),
            export_requested=metadata.get('export_requested', False),
            user_ip=user_data.get('ip'),
            user_agent=user_data.get('user_agent'),
            session_id=user_data.get('session_id'),
            response_length=len(response),
            temporal_analysis_used=metadata.get('temporal_analysis_used', False),
            oems_mentioned=self._extract_oems_mentioned(user_query),
            error_occurred=error_data.get('error_occurred', False),
            error_message=error_data.get('error_message')
        )
        
        # Save to log file
        self._append_to_log_file(query_log)
        
        # Update session tracking
        if user_data.get('session_id'):
            self._update_session_tracking(user_data.get('session_id'), query_log)
        
        # Update daily statistics
        self._update_daily_stats(query_log)
        
        return query_id
    
    def _extract_oems_mentioned(self, query: str) -> List[str]:
        """Extract OEM names mentioned in the query"""
        oems = ['Ola Electric', 'TVS iQube', 'Bajaj Chetak', 'Ather', 'Hero Vida']
        mentioned = []
        query_lower = query.lower()
        
        for oem in oems:
            if any(word.lower() in query_lower for word in oem.split()):
                mentioned.append(oem)
        
        return mentioned
    
    def _append_to_log_file(self, query_log: QueryLog):
        """Append query log to file"""
        try:
            # Load existing logs
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
            else:
                logs = []
            
            # Add new log
            logs.append(asdict(query_log))
            
            # Keep only last 1000 queries to avoid huge files
            if len(logs) > 1000:
                logs = logs[-1000:]
            
            # Save back to file
            with open(self.log_file, 'w', encoding='utf-8') as f:
                json.dump(logs, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"Error saving query log: {e}")
    
    def _update_session_tracking(self, session_id: str, query_log: QueryLog):
        """Update session tracking information"""
        try:
            # Load existing sessions
            if os.path.exists(self.session_file):
                with open(self.session_file, 'r', encoding='utf-8') as f:
                    sessions = json.load(f)
            else:
                sessions = {}
            
            # Update session
            if session_id not in sessions:
                sessions[session_id] = {
                    'first_query_time': query_log.timestamp,
                    'last_query_time': query_log.timestamp,
                    'total_queries': 0,
                    'total_processing_time': 0,
                    'unique_oems_queried': set(),
                    'export_requests': 0,
                    'errors': 0
                }
            
            session = sessions[session_id]
            session['last_query_time'] = query_log.timestamp
            session['total_queries'] += 1
            session['total_processing_time'] += query_log.processing_time
            
            # Convert set to list for JSON serialization
            if isinstance(session['unique_oems_queried'], set):
                session['unique_oems_queried'] = list(session['unique_oems_queried'])
            
            session['unique_oems_queried'].extend(query_log.oems_mentioned)
            session['unique_oems_queried'] = list(set(session['unique_oems_queried']))
            
            if query_log.export_requested:
                session['export_requests'] += 1
            if query_log.error_occurred:
                session['errors'] += 1
            
            # Save back to file
            with open(self.session_file, 'w', encoding='utf-8') as f:
                json.dump(sessions, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"Error updating session tracking: {e}")
    
    def _update_daily_stats(self, query_log: QueryLog):
        """Update daily statistics"""
        try:
            date_str = query_log.timestamp.split('T')[0]  # Get YYYY-MM-DD
            
            # Load existing stats
            if os.path.exists(self.daily_stats_file):
                with open(self.daily_stats_file, 'r', encoding='utf-8') as f:
                    daily_stats = json.load(f)
            else:
                daily_stats = {}
            
            # Initialize day if not exists
            if date_str not in daily_stats:
                daily_stats[date_str] = {
                    'total_queries': 0,
                    'total_processing_time': 0,
                    'avg_processing_time': 0,
                    'unique_users': 0,
                    'export_requests': 0,
                    'errors': 0,
                    'popular_oems': {},
                    'temporal_queries': 0,
                    'ai_analysis_queries': 0
                }
            
            stats = daily_stats[date_str]
            stats['total_queries'] += 1
            stats['total_processing_time'] += query_log.processing_time
            stats['avg_processing_time'] = stats['total_processing_time'] / stats['total_queries']
            
            if query_log.export_requested:
                stats['export_requests'] += 1
            if query_log.error_occurred:
                stats['errors'] += 1
            if query_log.temporal_analysis_used:
                stats['temporal_queries'] += 1
            if query_log.analysis_method == 'ai_powered':
                stats['ai_analysis_queries'] += 1
            
            # Track popular OEMs
            for oem in query_log.oems_mentioned:
                if oem not in stats['popular_oems']:
                    stats['popular_oems'][oem] = 0
                stats['popular_oems'][oem] += 1
            
            # Save back to file
            with open(self.daily_stats_file, 'w', encoding='utf-8') as f:
                json.dump(daily_stats, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"Error updating daily stats: {e}")
    
    def get_analytics_summary(self, days: int = 7) -> Dict[str, Any]:
        """Get analytics summary for the last N days"""
        try:
            # Load daily stats
            if not os.path.exists(self.daily_stats_file):
                return {"error": "No analytics data available"}
            
            with open(self.daily_stats_file, 'r', encoding='utf-8') as f:
                daily_stats = json.load(f)
            
            # Get recent dates
            from datetime import datetime, timedelta
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=days-1)
            
            # Aggregate statistics
            total_queries = 0
            total_processing_time = 0
            total_exports = 0
            total_errors = 0
            total_temporal = 0
            total_ai_analysis = 0
            popular_oems = {}
            daily_breakdown = {}
            
            for i in range(days):
                date = start_date + timedelta(days=i)
                date_str = date.isoformat()
                
                if date_str in daily_stats:
                    day_stats = daily_stats[date_str]
                    total_queries += day_stats.get('total_queries', 0)
                    total_processing_time += day_stats.get('total_processing_time', 0)
                    total_exports += day_stats.get('export_requests', 0)
                    total_errors += day_stats.get('errors', 0)
                    total_temporal += day_stats.get('temporal_queries', 0)
                    total_ai_analysis += day_stats.get('ai_analysis_queries', 0)
                    
                    # Aggregate OEM popularity
                    for oem, count in day_stats.get('popular_oems', {}).items():
                        if oem not in popular_oems:
                            popular_oems[oem] = 0
                        popular_oems[oem] += count
                    
                    daily_breakdown[date_str] = day_stats
            
            # Calculate averages
            avg_processing_time = total_processing_time / max(1, total_queries)
            error_rate = (total_errors / max(1, total_queries)) * 100
            export_rate = (total_exports / max(1, total_queries)) * 100
            temporal_rate = (total_temporal / max(1, total_queries)) * 100
            ai_analysis_rate = (total_ai_analysis / max(1, total_queries)) * 100
            
            return {
                "period": f"Last {days} days",
                "summary": {
                    "total_queries": total_queries,
                    "avg_processing_time": round(avg_processing_time, 2),
                    "error_rate": round(error_rate, 2),
                    "export_rate": round(export_rate, 2),
                    "temporal_analysis_rate": round(temporal_rate, 2),
                    "ai_analysis_rate": round(ai_analysis_rate, 2)
                },
                "popular_oems": dict(sorted(popular_oems.items(), key=lambda x: x[1], reverse=True)),
                "daily_breakdown": daily_breakdown
            }
            
        except Exception as e:
            return {"error": f"Error generating analytics summary: {e}"}
    
    def get_recent_queries(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent queries for monitoring"""
        try:
            if not os.path.exists(self.log_file):
                return []
            
            with open(self.log_file, 'r', encoding='utf-8') as f:
                logs = json.load(f)
            
            # Return most recent queries
            return logs[-limit:] if len(logs) > limit else logs
            
        except Exception as e:
            print(f"Error retrieving recent queries: {e}")
            return []
    
    def export_analytics_to_excel(self, output_file: str = None) -> str:
        """Export analytics data to Excel file"""
        try:
            import pandas as pd
            from datetime import datetime
            
            if not output_file:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_file = f"query_analytics_export_{timestamp}.xlsx"
            
            # Load data
            logs = self.get_recent_queries(1000)  # Get up to 1000 recent queries
            analytics = self.get_analytics_summary(30)  # Get 30-day summary
            
            # Create Excel writer
            with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
                # Query logs sheet
                if logs:
                    df_logs = pd.DataFrame(logs)
                    df_logs.to_excel(writer, sheet_name='Query_Logs', index=False)
                
                # Analytics summary sheet
                if 'daily_breakdown' in analytics:
                    df_daily = pd.DataFrame.from_dict(
                        analytics['daily_breakdown'], 
                        orient='index'
                    ).reset_index()
                    df_daily.rename(columns={'index': 'date'}, inplace=True)
                    df_daily.to_excel(writer, sheet_name='Daily_Analytics', index=False)
                
                # Popular OEMs sheet
                if 'popular_oems' in analytics:
                    df_oems = pd.DataFrame(
                        list(analytics['popular_oems'].items()),
                        columns=['OEM', 'Query_Count']
                    )
                    df_oems.to_excel(writer, sheet_name='Popular_OEMs', index=False)
            
            return output_file
            
        except Exception as e:
            print(f"Error exporting analytics to Excel: {e}")
            return None
