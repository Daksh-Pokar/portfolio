import streamlit as st
import pandas as pd
from utils.ai_generator import AIGenerator
from utils.data_processor import DataProcessor
import os
from datetime import datetime
import json

st.set_page_config(page_title="AI Reports", page_icon="🤖", layout="wide")

def main():
    st.title("🤖 AI-Powered Reports")
    st.markdown("Generate intelligent insights and automated reports from your data")
    
    # Check if AI services are available
    ai_generator = AIGenerator()
    
    if not ai_generator.is_available():
        st.warning("⚠️ AI services are not configured")
        st.info("""
        To enable AI-powered reports, please configure your OpenAI API key:
        - Set the OPENAI_API_KEY environment variable
        - Restart the application
        """)
        return
    
    # Initialize session state
    if 'report_history' not in st.session_state:
        st.session_state.report_history = []
    
    if 'current_data' not in st.session_state:
        st.session_state.current_data = None
    
    # Sidebar for data upload and settings
    with st.sidebar:
        st.header("Data & Settings")
        
        # Data upload
        uploaded_file = st.file_uploader(
            "Upload data for analysis",
            type=['csv', 'xlsx', 'json'],
            help="Upload your dataset to generate AI insights"
        )
        
        if uploaded_file is not None:
            try:
                processor = DataProcessor()
                st.session_state.current_data = processor.load_file(uploaded_file)
                st.success(f"Loaded {len(st.session_state.current_data)} rows")
                
                # Show basic data info
                with st.expander("Dataset Overview"):
                    st.write(f"**Rows:** {len(st.session_state.current_data)}")
                    st.write(f"**Columns:** {len(st.session_state.current_data.columns)}")
                    st.write("**Column Types:**")
                    for col, dtype in st.session_state.current_data.dtypes.items():
                        st.write(f"  • {col}: {dtype}")
                        
            except Exception as e:
                st.error(f"Error loading file: {str(e)}")
        
        st.markdown("---")
        
        # Report settings
        st.header("Report Settings")
        
        report_type = st.selectbox(
            "Report Type",
            options=[
                "Data Summary",
                "Trend Analysis",
                "Statistical Overview",
                "Correlation Analysis",
                "Custom Analysis"
            ]
        )
        
        analysis_depth = st.selectbox(
            "Analysis Depth",
            options=["Quick", "Standard", "Detailed"],
            index=1
        )
        
        include_visualizations = st.checkbox(
            "Include Visualization Suggestions",
            value=True
        )
    
    # Main content area
    if st.session_state.current_data is not None:
        
        # Data preview section
        st.header("📊 Data Overview")
        
        preview_col1, preview_col2 = st.columns([2, 1])
        
        with preview_col1:
            st.subheader("Data Preview")
            st.dataframe(st.session_state.current_data.head(10))
        
        with preview_col2:
            st.subheader("Quick Stats")
            st.metric("Total Rows", len(st.session_state.current_data))
            st.metric("Total Columns", len(st.session_state.current_data.columns))
            
            # Show missing values
            missing_data = st.session_state.current_data.isnull().sum()
            if missing_data.sum() > 0:
                st.metric("Missing Values", int(missing_data.sum()))
            else:
                st.metric("Missing Values", "None")
        
        # Custom query section
        st.markdown("---")
        st.header("🎯 Custom Analysis")
        
        query_col1, query_col2 = st.columns([3, 1])
        
        with query_col1:
            custom_query = st.text_area(
                "Ask a specific question about your data",
                placeholder="Example: What are the main trends in sales over time? Which factors correlate with customer satisfaction?",
                height=100
            )
        
        with query_col2:
            st.markdown("<br>", unsafe_allow_html=True)  # Add some spacing
            
            if st.button("Generate Report", use_container_width=True, type="primary"):
                if custom_query.strip():
                    generate_ai_report(
                        st.session_state.current_data,
                        custom_query,
                        report_type,
                        analysis_depth,
                        include_visualizations
                    )
                else:
                    st.error("Please enter a question or analysis request")
        
        # Pre-defined analysis buttons
        st.markdown("### 🚀 Quick Analysis Options")
        
        quick_col1, quick_col2, quick_col3 = st.columns(3)
        
        with quick_col1:
            if st.button("📈 Generate Data Summary", use_container_width=True):
                generate_ai_report(
                    st.session_state.current_data,
                    "Provide a comprehensive summary of this dataset including key statistics, patterns, and insights.",
                    "Data Summary",
                    analysis_depth,
                    include_visualizations
                )
        
        with quick_col2:
            if st.button("🔍 Find Correlations", use_container_width=True):
                generate_ai_report(
                    st.session_state.current_data,
                    "Analyze correlations between variables and identify significant relationships in the data.",
                    "Correlation Analysis",
                    analysis_depth,
                    include_visualizations
                )
        
        with quick_col3:
            if st.button("📊 Identify Trends", use_container_width=True):
                generate_ai_report(
                    st.session_state.current_data,
                    "Identify and analyze trends, patterns, and anomalies in the data over time or across categories.",
                    "Trend Analysis",
                    analysis_depth,
                    include_visualizations
                )
        
        # Report history section
        if st.session_state.report_history:
            st.markdown("---")
            st.header("📋 Report History")
            
            for i, report in enumerate(reversed(st.session_state.report_history)):
                with st.expander(f"Report {len(st.session_state.report_history) - i}: {report['title'][:50]}..."):
                    st.markdown(f"**Generated:** {report['timestamp']}")
                    st.markdown(f"**Type:** {report['type']}")
                    st.markdown(f"**Query:** {report['query']}")
                    st.markdown("**Analysis:**")
                    st.markdown(report['content'])
                    
                    # Download button for each report
                    report_text = f"""
# {report['title']}

**Generated:** {report['timestamp']}
**Type:** {report['type']}
**Query:** {report['query']}

## Analysis

{report['content']}
"""
                    st.download_button(
                        label="Download Report",
                        data=report_text,
                        file_name=f"ai_report_{i+1}.md",
                        mime="text/markdown",
                        key=f"download_{i}"
                    )
    
    else:
        # No data state
        st.info("📁 Please upload a dataset using the sidebar to get started with AI analysis")
        
        # Show capabilities
        st.markdown("### 🎯 AI Analysis Capabilities")
        
        cap_col1, cap_col2 = st.columns(2)
        
        with cap_col1:
            st.markdown("""
            **Automated Insights:**
            - 📊 Statistical summaries
            - 📈 Trend identification
            - 🔍 Pattern recognition
            - 📉 Anomaly detection
            """)
        
        with cap_col2:
            st.markdown("""
            **Advanced Analysis:**
            - 🔗 Correlation analysis
            - 🎯 Predictive insights
            - 📋 Custom queries
            - 💡 Recommendations
            """)

def generate_ai_report(data, query, report_type, depth, include_viz):
    """Generate an AI-powered report based on the data and query"""
    
    with st.spinner("🤖 Generating AI report..."):
        try:
            ai_generator = AIGenerator()
            
            # Generate the report
            report_content = ai_generator.generate_report(
                data=data,
                query=query,
                report_type=report_type,
                depth=depth,
                include_visualizations=include_viz
            )
            
            if report_content:
                # Create report entry
                report_entry = {
                    'title': query[:100],
                    'content': report_content,
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'type': report_type,
                    'query': query
                }
                
                # Add to history
                st.session_state.report_history.append(report_entry)
                
                # Display the report
                st.markdown("---")
                st.success("✅ Report generated successfully!")
                
                st.markdown("### 📄 Generated Report")
                
                # Report metadata
                meta_col1, meta_col2, meta_col3 = st.columns(3)
                with meta_col1:
                    st.metric("Report Type", report_type)
                with meta_col2:
                    st.metric("Analysis Depth", depth)
                with meta_col3:
                    st.metric("Generated", "Just now")
                
                # Report content
                st.markdown("#### Analysis Results")
                st.markdown(report_content)
                
                # Download option
                report_text = f"""
# AI Data Analysis Report

**Generated:** {report_entry['timestamp']}
**Type:** {report_type}
**Analysis Depth:** {depth}
**Query:** {query}

## Analysis Results

{report_content}
"""
                st.download_button(
                    label="📥 Download Report",
                    data=report_text,
                    file_name=f"ai_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                    mime="text/markdown",
                    use_container_width=True
                )
                
            else:
                st.error("❌ Failed to generate report. Please try again.")
                
        except Exception as e:
            st.error(f"❌ Error generating report: {str(e)}")

if __name__ == "__main__":
    main()
