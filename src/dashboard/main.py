"""
Main Dashboard Application for Telugu Story Engine
Advanced real-time dashboard with comprehensive monitoring
"""

import asyncio
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from streamlit_autorefresh import st_autorefresh
import requests
import json

from ..core.config import get_config
from ..core.model_manager import get_model_manager
# Components will be imported as they are implemented
# from .components import (...)

logger = logging.getLogger(__name__)

class TeluguStoryDashboard:
    """Advanced Dashboard for Telugu Story Engine"""
    
    def __init__(self):
        self.config = get_config()
        self.api_base_url = f"http://{self.config.api.host}:{self.config.api.port}/api/v2"
        self.refresh_interval = 5000  # 5 seconds
        
        # Initialize session state
        if 'dashboard_data' not in st.session_state:
            st.session_state.dashboard_data = {}
        
        if 'last_update' not in st.session_state:
            st.session_state.last_update = datetime.now()
    
    def run(self):
        """Run the dashboard"""
        st.set_page_config(
            page_title="Telugu Story Engine Dashboard",
            page_icon="📚",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Auto-refresh
        st_autorefresh(interval=self.refresh_interval, key="dashboard_refresh")
        
        # Main dashboard
        self.render_dashboard()
    
    def render_dashboard(self):
        """Render the main dashboard"""
        # Header
        st.title("🎭 Telugu Story Engine Dashboard")
        st.markdown("**Real-time monitoring and analytics for AI-powered Telugu story generation**")
        
        # Sidebar
        self.render_sidebar()
        
        # Main content
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📊 Overview", 
            "🤖 Models", 
            "👥 Agents", 
            "📖 Stories", 
            "⚡ Performance", 
            "📋 Logs"
        ])
        
        with tab1:
            self.render_overview_tab()
        
        with tab2:
            self.render_models_tab()
        
        with tab3:
            self.render_agents_tab()
        
        with tab4:
            self.render_stories_tab()
        
        with tab5:
            self.render_performance_tab()
        
        with tab6:
            self.render_logs_tab()
    
    def render_sidebar(self):
        """Render sidebar with controls and status"""
        st.sidebar.header("🎛️ Dashboard Controls")
        
        # System status
        system_status = self.get_system_status()
        if system_status:
            status_color = "🟢" if system_status.get("status") == "healthy" else "🔴"
            st.sidebar.metric(
                "System Status",
                f"{status_color} {system_status.get('status', 'Unknown').title()}",
                f"Uptime: {self.format_uptime(system_status.get('uptime', 0))}"
            )
        
        # Refresh controls
        st.sidebar.subheader("🔄 Refresh Settings")
        auto_refresh = st.sidebar.checkbox("Auto Refresh", value=True)
        
        if not auto_refresh:
            if st.sidebar.button("Manual Refresh"):
                st.rerun()
        
        refresh_rate = st.sidebar.selectbox(
            "Refresh Rate",
            [1, 5, 10, 30, 60],
            index=1,
            format_func=lambda x: f"{x} seconds"
        )
        
        # Model controls
        st.sidebar.subheader("🤖 Model Controls")
        if st.sidebar.button("Reload Models"):
            self.reload_models()
        
        if st.sidebar.button("Clear Cache"):
            self.clear_cache()
        
        # Export data
        st.sidebar.subheader("📤 Export")
        if st.sidebar.button("Export Metrics"):
            self.export_metrics()
        
        # Last update time
        st.sidebar.markdown("---")
        st.sidebar.caption(f"Last updated: {st.session_state.last_update.strftime('%H:%M:%S')}")
    
    def render_overview_tab(self):
        """Render overview tab"""
        st.header("📊 System Overview")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        metrics = self.get_dashboard_metrics()
        
        with col1:
            st.metric(
                "Stories Generated",
                metrics.get("total_stories", 0),
                delta=metrics.get("stories_today", 0)
            )
        
        with col2:
            st.metric(
                "Success Rate",
                f"{metrics.get('success_rate', 0):.1%}",
                delta=f"{metrics.get('success_rate_change', 0):+.1%}"
            )
        
        with col3:
            st.metric(
                "Avg Generation Time",
                f"{metrics.get('avg_generation_time', 0):.1f}s",
                delta=f"{metrics.get('time_change', 0):+.1f}s"
            )
        
        with col4:
            st.metric(
                "Active Users",
                metrics.get("active_users", 0),
                delta=metrics.get("user_change", 0)
            )
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            self.render_story_generation_chart()
        
        with col2:
            self.render_cultural_context_chart()
        
        # Recent activity
        st.subheader("📈 Recent Activity")
        self.render_recent_activity()
    
    def render_models_tab(self):
        """Render models tab"""
        st.header("🤖 AI Models Status")
        
        model_info = self.get_model_info()
        
        if model_info:
            # Model status overview
            col1, col2, col3 = st.columns(3)
            
            loaded_models = sum(1 for info in model_info.values() if info.get("loaded", False))
            total_models = len(model_info)
            total_memory = sum(info.get("memory_usage", 0) for info in model_info.values())
            
            with col1:
                st.metric("Loaded Models", f"{loaded_models}/{total_models}")
            
            with col2:
                st.metric("Total Memory", f"{total_memory:.1f} MB")
            
            with col3:
                avg_load_time = np.mean([
                    info.get("load_time", 0) for info in model_info.values() 
                    if info.get("load_time", 0) > 0
                ])
                st.metric("Avg Load Time", f"{avg_load_time:.1f}s")
            
            # Model details
            st.subheader("📋 Model Details")
            
            for model_name, info in model_info.items():
                with st.expander(f"🔧 {model_name}"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        status = "✅ Loaded" if info.get("loaded") else "❌ Not Loaded"
                        st.write(f"**Status:** {status}")
                        st.write(f"**Type:** {info.get('model_type', 'Unknown')}")
                    
                    with col2:
                        st.write(f"**Parameters:** {info.get('parameters', 0):,}")
                        st.write(f"**Memory:** {info.get('memory_usage', 0):.1f} MB")
                    
                    with col3:
                        load_time = info.get('load_time', 0)
                        st.write(f"**Load Time:** {load_time:.1f}s")
                        
                        if st.button(f"Reload {model_name}", key=f"reload_{model_name}"):
                            self.reload_specific_model(model_name)
            
            # Model performance chart
            st.subheader("📊 Model Performance")
            self.render_model_performance_chart()
        
        else:
            st.warning("Unable to fetch model information")
    
    def render_agents_tab(self):
        """Render agents tab"""
        st.header("👥 Multi-Agent System")
        
        agent_status = self.get_agent_status()
        
        if agent_status:
            # Agent overview
            col1, col2, col3, col4 = st.columns(4)
            
            active_agents = len([a for a in agent_status if a.get("status") == "active"])
            total_agents = len(agent_status)
            avg_confidence = np.mean([a.get("confidence", 0) for a in agent_status])
            total_memory = sum(a.get("memory_usage", 0) for a in agent_status)
            
            with col1:
                st.metric("Active Agents", f"{active_agents}/{total_agents}")
            
            with col2:
                st.metric("Avg Confidence", f"{avg_confidence:.2f}")
            
            with col3:
                st.metric("Total Memory", f"{total_memory:.1f} MB")
            
            with col4:
                processing_agents = len([a for a in agent_status if a.get("status") == "processing"])
                st.metric("Processing", processing_agents)
            
            # Agent details
            st.subheader("🤖 Agent Status")
            
            for agent in agent_status:
                with st.expander(f"🎭 {agent.get('agent_type', 'Unknown Agent')}"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        status_emoji = {
                            "active": "🟢",
                            "processing": "🟡", 
                            "idle": "⚪",
                            "error": "🔴"
                        }.get(agent.get("status"), "❓")
                        
                        st.write(f"**Status:** {status_emoji} {agent.get('status', 'Unknown')}")
                        st.write(f"**ID:** {agent.get('agent_id', 'N/A')[:8]}...")
                    
                    with col2:
                        st.write(f"**Confidence:** {agent.get('confidence', 0):.2f}")
                        st.write(f"**Processing Time:** {agent.get('processing_time', 0):.2f}s")
                    
                    with col3:
                        st.write(f"**Memory:** {agent.get('memory_usage', 0):.1f} MB")
                        current_task = agent.get('current_task', 'None')
                        st.write(f"**Current Task:** {current_task}")
            
            # Agent collaboration chart
            st.subheader("🤝 Agent Collaboration")
            self.render_agent_collaboration_chart()
        
        else:
            st.warning("Unable to fetch agent status")
    
    def render_stories_tab(self):
        """Render stories tab"""
        st.header("📖 Story Analytics")
        
        # Story metrics
        story_metrics = self.get_story_metrics()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total Stories",
                story_metrics.get("total_stories", 0),
                delta=story_metrics.get("stories_change", 0)
            )
        
        with col2:
            st.metric(
                "Avg Quality Score",
                f"{story_metrics.get('avg_quality', 0):.2f}",
                delta=f"{story_metrics.get('quality_change', 0):+.2f}"
            )
        
        with col3:
            st.metric(
                "Cultural Authenticity",
                f"{story_metrics.get('avg_cultural_score', 0):.2f}",
                delta=f"{story_metrics.get('cultural_change', 0):+.2f}"
            )
        
        with col4:
            st.metric(
                "Avg Word Count",
                f"{story_metrics.get('avg_word_count', 0):,.0f}",
                delta=f"{story_metrics.get('word_count_change', 0):+.0f}"
            )
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Story Types Distribution")
            self.render_story_types_chart()
        
        with col2:
            st.subheader("🌍 Cultural Context Distribution")
            self.render_cultural_distribution_chart()
        
        # Recent stories
        st.subheader("📚 Recent Stories")
        self.render_recent_stories()
    
    def render_performance_tab(self):
        """Render performance tab"""
        st.header("⚡ Performance Metrics")
        
        # Performance overview
        perf_metrics = self.get_performance_metrics()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Requests/min",
                perf_metrics.get("requests_per_minute", 0),
                delta=perf_metrics.get("requests_change", 0)
            )
        
        with col2:
            st.metric(
                "Avg Response Time",
                f"{perf_metrics.get('avg_response_time', 0):.2f}s",
                delta=f"{perf_metrics.get('response_time_change', 0):+.2f}s"
            )
        
        with col3:
            st.metric(
                "Error Rate",
                f"{perf_metrics.get('error_rate', 0):.1%}",
                delta=f"{perf_metrics.get('error_rate_change', 0):+.1%}"
            )
        
        with col4:
            st.metric(
                "System Load",
                f"{perf_metrics.get('system_load', 0):.1%}",
                delta=f"{perf_metrics.get('load_change', 0):+.1%}"
            )
        
        # Performance charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Response Time Trend")
            self.render_response_time_chart()
        
        with col2:
            st.subheader("💾 Memory Usage")
            self.render_memory_usage_chart()
        
        # Detailed metrics
        st.subheader("📊 Detailed Performance Metrics")
        self.render_detailed_performance_table()
    
    def render_logs_tab(self):
        """Render logs tab"""
        st.header("📋 System Logs")
        
        # Log controls
        col1, col2, col3 = st.columns(3)
        
        with col1:
            log_level = st.selectbox("Log Level", ["ALL", "ERROR", "WARNING", "INFO", "DEBUG"])
        
        with col2:
            log_source = st.selectbox("Source", ["ALL", "API", "AGENTS", "MODELS", "DASHBOARD"])
        
        with col3:
            max_logs = st.number_input("Max Logs", min_value=10, max_value=1000, value=100)
        
        # Real-time logs
        st.subheader("🔄 Real-time Logs")
        logs_container = st.container()
        
        with logs_container:
            logs = self.get_recent_logs(log_level, log_source, max_logs)
            
            if logs:
                for log in logs:
                    level_emoji = {
                        "ERROR": "🔴",
                        "WARNING": "🟡",
                        "INFO": "🔵",
                        "DEBUG": "⚪"
                    }.get(log.get("level", "INFO"), "⚪")
                    
                    timestamp = log.get("timestamp", "")
                    source = log.get("source", "")
                    message = log.get("message", "")
                    
                    st.text(f"{level_emoji} [{timestamp}] {source}: {message}")
            else:
                st.info("No logs available")
    
    # Data fetching methods
    def get_system_status(self) -> Optional[Dict[str, Any]]:
        """Get system status from API"""
        try:
            response = requests.get(f"{self.api_base_url}/system/status", timeout=5)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            logger.error(f"Failed to fetch system status: {e}")
        return None
    
    def get_dashboard_metrics(self) -> Dict[str, Any]:
        """Get dashboard metrics"""
        try:
            response = requests.get(f"{self.api_base_url}/dashboard/metrics", timeout=5)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            logger.error(f"Failed to fetch dashboard metrics: {e}")
        
        # Return mock data for development
        return {
            "total_stories": 1247,
            "stories_today": 23,
            "success_rate": 0.94,
            "success_rate_change": 0.02,
            "avg_generation_time": 12.3,
            "time_change": -0.5,
            "active_users": 15,
            "user_change": 3
        }
    
    def get_model_info(self) -> Optional[Dict[str, Any]]:
        """Get model information"""
        try:
            response = requests.get(f"{self.api_base_url}/models/info", timeout=5)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            logger.error(f"Failed to fetch model info: {e}")
        
        # Return mock data for development
        return {
            "telugu_bert": {
                "loaded": True,
                "model_type": "text_understanding",
                "parameters": 110000000,
                "memory_usage": 450.2,
                "load_time": 8.5
            },
            "telugu_gpt": {
                "loaded": True,
                "model_type": "text_generation", 
                "parameters": 774000000,
                "memory_usage": 1200.8,
                "load_time": 15.2
            },
            "emotion_model": {
                "loaded": True,
                "model_type": "emotion_classification",
                "parameters": 67000000,
                "memory_usage": 280.5,
                "load_time": 4.1
            }
        }
    
    def get_agent_status(self) -> Optional[List[Dict[str, Any]]]:
        """Get agent status"""
        try:
            response = requests.get(f"{self.api_base_url}/agents/status", timeout=5)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            logger.error(f"Failed to fetch agent status: {e}")
        
        # Return mock data for development
        return [
            {
                "agent_id": "story-struct-001",
                "agent_type": "StoryStructureAgent",
                "status": "active",
                "confidence": 0.89,
                "processing_time": 2.3,
                "memory_usage": 45.2,
                "current_task": "plot_development"
            },
            {
                "agent_id": "emotion-intel-001",
                "agent_type": "EmotionalIntelligenceAgent",
                "status": "processing",
                "confidence": 0.92,
                "processing_time": 1.8,
                "memory_usage": 38.7,
                "current_task": "emotion_analysis"
            },
            {
                "agent_id": "cultural-adapt-001",
                "agent_type": "CulturalAdaptationAgent",
                "status": "idle",
                "confidence": 0.85,
                "processing_time": 0.0,
                "memory_usage": 32.1,
                "current_task": None
            }
        ]
    
    def get_story_metrics(self) -> Dict[str, Any]:
        """Get story metrics"""
        # Mock data for development
        return {
            "total_stories": 1247,
            "stories_change": 23,
            "avg_quality": 4.2,
            "quality_change": 0.1,
            "avg_cultural_score": 4.5,
            "cultural_change": 0.05,
            "avg_word_count": 2150,
            "word_count_change": 50
        }
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics"""
        # Mock data for development
        return {
            "requests_per_minute": 12,
            "requests_change": 2,
            "avg_response_time": 1.8,
            "response_time_change": -0.2,
            "error_rate": 0.02,
            "error_rate_change": -0.005,
            "system_load": 0.65,
            "load_change": 0.05
        }
    
    def get_recent_logs(self, level: str, source: str, max_logs: int) -> List[Dict[str, Any]]:
        """Get recent logs"""
        # Mock data for development
        return [
            {
                "timestamp": "2024-01-15 10:30:25",
                "level": "INFO",
                "source": "API",
                "message": "Story generation request received"
            },
            {
                "timestamp": "2024-01-15 10:30:24",
                "level": "DEBUG",
                "source": "AGENTS",
                "message": "StoryStructureAgent processing started"
            },
            {
                "timestamp": "2024-01-15 10:30:23",
                "level": "WARNING",
                "source": "MODELS",
                "message": "High memory usage detected for telugu_gpt model"
            }
        ]
    
    # Chart rendering methods
    def render_story_generation_chart(self):
        """Render story generation trend chart"""
        # Generate sample data
        dates = pd.date_range(start='2024-01-01', end='2024-01-15', freq='D')
        stories = np.random.poisson(15, len(dates))
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dates,
            y=stories,
            mode='lines+markers',
            name='Stories Generated',
            line=dict(color='#1f77b4', width=2)
        ))
        
        fig.update_layout(
            title="Daily Story Generation",
            xaxis_title="Date",
            yaxis_title="Stories Generated",
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def render_cultural_context_chart(self):
        """Render cultural context distribution chart"""
        contexts = ['Contemporary', 'Traditional', 'Rural', 'Coastal', 'Telangana']
        values = [45, 25, 15, 10, 5]
        
        fig = go.Figure(data=[go.Pie(
            labels=contexts,
            values=values,
            hole=0.3
        )])
        
        fig.update_layout(
            title="Cultural Context Distribution",
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def render_recent_activity(self):
        """Render recent activity table"""
        activities = [
            {"Time": "10:30:25", "Activity": "Story generated", "User": "user123", "Status": "✅"},
            {"Time": "10:29:18", "Activity": "Model loaded", "User": "system", "Status": "✅"},
            {"Time": "10:28:45", "Activity": "Agent collaboration", "User": "user456", "Status": "🔄"},
            {"Time": "10:27:32", "Activity": "Cache cleared", "User": "admin", "Status": "✅"},
            {"Time": "10:26:15", "Activity": "Story analysis", "User": "user789", "Status": "✅"}
        ]
        
        df = pd.DataFrame(activities)
        st.dataframe(df, use_container_width=True)
    
    # Utility methods
    def format_uptime(self, uptime_seconds: float) -> str:
        """Format uptime in human readable format"""
        if uptime_seconds < 60:
            return f"{uptime_seconds:.0f}s"
        elif uptime_seconds < 3600:
            return f"{uptime_seconds/60:.0f}m"
        elif uptime_seconds < 86400:
            return f"{uptime_seconds/3600:.1f}h"
        else:
            return f"{uptime_seconds/86400:.1f}d"
    
    def reload_models(self):
        """Reload all models"""
        try:
            response = requests.post(f"{self.api_base_url}/models/reload", timeout=30)
            if response.status_code == 200:
                st.success("Models reloaded successfully")
            else:
                st.error("Failed to reload models")
        except Exception as e:
            st.error(f"Error reloading models: {e}")
    
    def clear_cache(self):
        """Clear system cache"""
        try:
            response = requests.post(f"{self.api_base_url}/system/clear-cache", timeout=10)
            if response.status_code == 200:
                st.success("Cache cleared successfully")
            else:
                st.error("Failed to clear cache")
        except Exception as e:
            st.error(f"Error clearing cache: {e}")
    
    def export_metrics(self):
        """Export metrics to file"""
        try:
            metrics = {
                "system_status": self.get_system_status(),
                "dashboard_metrics": self.get_dashboard_metrics(),
                "model_info": self.get_model_info(),
                "agent_status": self.get_agent_status(),
                "timestamp": datetime.now().isoformat()
            }
            
            # Convert to JSON and offer download
            json_str = json.dumps(metrics, indent=2)
            st.download_button(
                label="Download Metrics JSON",
                data=json_str,
                file_name=f"telugu_story_engine_metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        except Exception as e:
            st.error(f"Error exporting metrics: {e}")

def create_dashboard_app():
    """Create and return the dashboard app"""
    dashboard = TeluguStoryDashboard()
    return dashboard.run

def main():
    """Main function to run the dashboard"""
    dashboard = TeluguStoryDashboard()
    dashboard.run()

if __name__ == "__main__":
    main()