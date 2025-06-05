import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os

# Configure page
st.set_page_config(
    page_title="DataFlow Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main app
def main():
    st.title("📊 DataFlow Analytics")
    st.markdown("### Professional Data Dashboard & Report Builder")
    
    # Main navigation info
    st.markdown("""
    Welcome to DataFlow Analytics - your comprehensive data visualization and reporting platform.
    
    **Available Tools:**
    - 🏗️ **Dashboard Builder**: Create custom interactive dashboards
    - 🤖 **AI Reports**: Generate automated reports using AI
    - 🔗 **Data Sources**: Connect and manage your data sources
    """)
    
    # Quick stats section
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Active Dashboards",
            value="0",
            help="Number of active dashboards in your workspace"
        )
    
    with col2:
        st.metric(
            label="Data Sources",
            value="0",
            help="Connected data sources"
        )
    
    with col3:
        st.metric(
            label="AI Reports Generated",
            value="0",
            help="Total AI-generated reports"
        )
    
    with col4:
        st.metric(
            label="Last Updated",
            value="Never",
            help="Last data refresh"
        )
    
    # Getting started section
    st.markdown("---")
    st.markdown("### 🚀 Getting Started")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Step 1: Connect Your Data**
        - Upload CSV/Excel files
        - Connect to databases
        - Configure API endpoints
        """)
        
        if st.button("Connect Data Sources", use_container_width=True):
            st.switch_page("pages/3_Data_Sources.py")
    
    with col2:
        st.markdown("""
        **Step 2: Build Dashboards**
        - Create interactive visualizations
        - Design custom layouts
        - Configure real-time updates
        """)
        
        if st.button("Build Dashboard", use_container_width=True):
            st.switch_page("pages/1_Dashboard_Builder.py")
    
    # Feature highlights
    st.markdown("---")
    st.markdown("### ✨ Key Features")
    
    feature_col1, feature_col2, feature_col3 = st.columns(3)
    
    with feature_col1:
        st.markdown("""
        **🎨 Custom Dashboards**
        - Drag-and-drop interface
        - Multiple chart types
        - Real-time data updates
        - Interactive filters
        """)
    
    with feature_col2:
        st.markdown("""
        **🤖 AI-Powered Insights**
        - Automated report generation
        - Intelligent data analysis
        - Natural language queries
        - Predictive analytics
        """)
    
    with feature_col3:
        st.markdown("""
        **🔗 Data Integration**
        - Multiple data sources
        - Real-time connections
        - Data transformation
        - Secure access controls
        """)
    
    # Status check
    st.markdown("---")
    st.markdown("### 🔧 System Status")
    
    status_col1, status_col2 = st.columns(2)
    
    with status_col1:
        # Check if API keys are configured
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key:
            st.success("✅ AI Services: Connected")
        else:
            st.warning("⚠️ AI Services: API key not configured")
            st.info("Add OPENAI_API_KEY to environment variables to enable AI features")
    
    with status_col2:
        st.success("✅ Core Services: Online")
        st.info("All dashboard and data processing services are operational")

if __name__ == "__main__":
    main()
