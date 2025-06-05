import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from utils.dashboard_components import DashboardComponents
from utils.data_processor import DataProcessor
import json

st.set_page_config(page_title="Dashboard Builder", page_icon="🏗️", layout="wide")

def main():
    st.title("🏗️ Dashboard Builder")
    st.markdown("Create and customize your data dashboards")
    
    # Initialize session state
    if 'dashboard_config' not in st.session_state:
        st.session_state.dashboard_config = {
            'charts': [],
            'layout': 'grid',
            'title': 'New Dashboard'
        }
    
    if 'uploaded_data' not in st.session_state:
        st.session_state.uploaded_data = None
    
    # Sidebar for dashboard configuration
    with st.sidebar:
        st.header("Dashboard Settings")
        
        # Dashboard title
        dashboard_title = st.text_input(
            "Dashboard Title", 
            value=st.session_state.dashboard_config['title']
        )
        st.session_state.dashboard_config['title'] = dashboard_title
        
        # Layout options
        layout_option = st.selectbox(
            "Layout Style",
            options=['grid', 'single_column', 'two_column'],
            index=['grid', 'single_column', 'two_column'].index(
                st.session_state.dashboard_config['layout']
            )
        )
        st.session_state.dashboard_config['layout'] = layout_option
        
        st.markdown("---")
        
        # Data upload section
        st.header("Data Source")
        uploaded_file = st.file_uploader(
            "Upload your data",
            type=['csv', 'xlsx', 'json'],
            help="Upload a CSV, Excel, or JSON file to get started"
        )
        
        if uploaded_file is not None:
            try:
                processor = DataProcessor()
                st.session_state.uploaded_data = processor.load_file(uploaded_file)
                st.success(f"Loaded {len(st.session_state.uploaded_data)} rows")
                
                # Show data preview
                with st.expander("Data Preview"):
                    st.dataframe(st.session_state.uploaded_data.head())
                    
            except Exception as e:
                st.error(f"Error loading file: {str(e)}")
    
    # Main dashboard area
    if st.session_state.uploaded_data is not None:
        # Chart builder section
        st.header("📊 Add Charts")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            chart_type = st.selectbox(
                "Chart Type",
                options=['line', 'bar', 'scatter', 'histogram', 'box', 'pie']
            )
        
        with col2:
            numeric_columns = st.session_state.uploaded_data.select_dtypes(
                include=[np.number]
            ).columns.tolist()
            
            if numeric_columns:
                y_column = st.selectbox("Y-axis", options=numeric_columns)
            else:
                st.warning("No numeric columns found for Y-axis")
                y_column = None
        
        with col3:
            all_columns = st.session_state.uploaded_data.columns.tolist()
            x_column = st.selectbox("X-axis", options=all_columns)
        
        # Additional chart options
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            chart_title = st.text_input("Chart Title", value=f"{chart_type.title()} Chart")
        
        with chart_col2:
            color_column = st.selectbox(
                "Color By (Optional)", 
                options=[None] + all_columns,
                index=0
            )
        
        # Add chart button
        if st.button("Add Chart to Dashboard", use_container_width=True):
            if y_column or chart_type in ['histogram', 'pie']:
                chart_config = {
                    'type': chart_type,
                    'x': x_column,
                    'y': y_column,
                    'color': color_column,
                    'title': chart_title,
                    'id': len(st.session_state.dashboard_config['charts'])
                }
                st.session_state.dashboard_config['charts'].append(chart_config)
                st.success(f"Added {chart_title} to dashboard")
                st.rerun()
            else:
                st.error("Please select a Y-axis column for this chart type")
        
        # Dashboard preview
        st.markdown("---")
        st.header(f"📋 {dashboard_title}")
        
        if st.session_state.dashboard_config['charts']:
            components = DashboardComponents()
            
            # Render charts based on layout
            if layout_option == 'single_column':
                for chart_config in st.session_state.dashboard_config['charts']:
                    components.render_chart(st.session_state.uploaded_data, chart_config)
                    
            elif layout_option == 'two_column':
                chart_pairs = [
                    st.session_state.dashboard_config['charts'][i:i+2] 
                    for i in range(0, len(st.session_state.dashboard_config['charts']), 2)
                ]
                
                for pair in chart_pairs:
                    cols = st.columns(len(pair))
                    for i, chart_config in enumerate(pair):
                        with cols[i]:
                            components.render_chart(st.session_state.uploaded_data, chart_config)
                            
            else:  # grid layout
                chart_groups = [
                    st.session_state.dashboard_config['charts'][i:i+3] 
                    for i in range(0, len(st.session_state.dashboard_config['charts']), 3)
                ]
                
                for group in chart_groups:
                    cols = st.columns(len(group))
                    for i, chart_config in enumerate(group):
                        with cols[i]:
                            components.render_chart(st.session_state.uploaded_data, chart_config)
            
            # Dashboard management
            st.markdown("---")
            mgmt_col1, mgmt_col2, mgmt_col3 = st.columns(3)
            
            with mgmt_col1:
                if st.button("Clear All Charts", use_container_width=True):
                    st.session_state.dashboard_config['charts'] = []
                    st.rerun()
            
            with mgmt_col2:
                # Export dashboard configuration
                config_json = json.dumps(st.session_state.dashboard_config, indent=2)
                st.download_button(
                    label="Export Configuration",
                    data=config_json,
                    file_name=f"{dashboard_title.replace(' ', '_')}_config.json",
                    mime="application/json",
                    use_container_width=True
                )
            
            with mgmt_col3:
                st.info(f"Charts: {len(st.session_state.dashboard_config['charts'])}")
        
        else:
            st.info("👆 Add charts using the form above to build your dashboard")
    
    else:
        # No data uploaded state
        st.info("📁 Please upload a data file using the sidebar to get started")
        
        # Show sample data structure
        st.markdown("### 📋 Supported Data Formats")
        
        format_col1, format_col2 = st.columns(2)
        
        with format_col1:
            st.markdown("""
            **CSV Example:**
            ```
            date,sales,region
            2024-01-01,1000,North
            2024-01-02,1200,South
            2024-01-03,950,East
            ```
            """)
        
        with format_col2:
            st.markdown("""
            **Supported Formats:**
            - 📊 CSV files (.csv)
            - 📗 Excel files (.xlsx)
            - 🔧 JSON files (.json)
            """)

if __name__ == "__main__":
    main()
