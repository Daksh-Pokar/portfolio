import streamlit as st
import pandas as pd
import sqlite3
import json
from utils.data_processor import DataProcessor
from datetime import datetime
import os

st.set_page_config(page_title="Data Sources", page_icon="🔗", layout="wide")

def main():
    st.title("🔗 Data Sources")
    st.markdown("Connect and manage your data sources for dashboard and reporting")
    
    # Initialize session state
    if 'connected_sources' not in st.session_state:
        st.session_state.connected_sources = []
    
    if 'sample_data' not in st.session_state:
        st.session_state.sample_data = create_sample_datasets()
    
    # Sidebar for connection options
    with st.sidebar:
        st.header("Connection Options")
        
        source_type = st.selectbox(
            "Select Data Source Type",
            options=[
                "File Upload",
                "Database Connection",
                "API Endpoint",
                "Sample Data"
            ]
        )
        
        st.markdown("---")
        st.header("Active Connections")
        
        if st.session_state.connected_sources:
            for i, source in enumerate(st.session_state.connected_sources):
                with st.expander(f"{source['name']}"):
                    st.write(f"**Type:** {source['type']}")
                    st.write(f"**Status:** {source['status']}")
                    st.write(f"**Records:** {source.get('record_count', 'Unknown')}")
                    st.write(f"**Connected:** {source['connected_at']}")
                    
                    if st.button(f"Remove {source['name']}", key=f"remove_{i}"):
                        st.session_state.connected_sources.pop(i)
                        st.rerun()
        else:
            st.info("No active connections")
    
    # Main content area based on selected source type
    if source_type == "File Upload":
        handle_file_upload()
    elif source_type == "Database Connection":
        handle_database_connection()
    elif source_type == "API Endpoint":
        handle_api_connection()
    elif source_type == "Sample Data":
        handle_sample_data()

def handle_file_upload():
    """Handle file upload data source"""
    st.header("📁 File Upload")
    st.markdown("Upload CSV, Excel, or JSON files to use as data sources")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=['csv', 'xlsx', 'json'],
        help="Supported formats: CSV, Excel (.xlsx), JSON"
    )
    
    if uploaded_file is not None:
        try:
            processor = DataProcessor()
            data = processor.load_file(uploaded_file)
            
            # Display file information
            info_col1, info_col2, info_col3 = st.columns(3)
            
            with info_col1:
                st.metric("File Size", f"{uploaded_file.size / 1024:.1f} KB")
            with info_col2:
                st.metric("Rows", len(data))
            with info_col3:
                st.metric("Columns", len(data.columns))
            
            # Data preview
            st.subheader("Data Preview")
            st.dataframe(data.head(10))
            
            # Column information
            st.subheader("Column Information")
            col_info = pd.DataFrame({
                'Column': data.columns,
                'Type': data.dtypes.astype(str),
                'Non-Null': data.count(),
                'Null Count': data.isnull().sum(),
                'Sample Values': [str(data[col].dropna().iloc[0]) if not data[col].dropna().empty else 'N/A' for col in data.columns]
            })
            st.dataframe(col_info)
            
            # Connection options
            st.subheader("Connection Settings")
            
            conn_col1, conn_col2 = st.columns(2)
            
            with conn_col1:
                connection_name = st.text_input(
                    "Connection Name",
                    value=uploaded_file.name.split('.')[0]
                )
            
            with conn_col2:
                auto_refresh = st.checkbox("Enable Auto Refresh", help="Automatically refresh data when file is updated")
            
            # Add connection button
            if st.button("Add Data Source", use_container_width=True, type="primary"):
                source_config = {
                    'name': connection_name,
                    'type': 'File Upload',
                    'status': 'Connected',
                    'file_name': uploaded_file.name,
                    'record_count': len(data),
                    'columns': list(data.columns),
                    'connected_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'auto_refresh': auto_refresh,
                    'data': data  # Store data in session for demo purposes
                }
                
                st.session_state.connected_sources.append(source_config)
                st.success(f"✅ Successfully connected '{connection_name}'")
                st.rerun()
                
        except Exception as e:
            st.error(f"❌ Error loading file: {str(e)}")

def handle_database_connection():
    """Handle database connection setup"""
    st.header("🗄️ Database Connection")
    st.markdown("Connect to SQL databases for real-time data access")
    
    # Database type selection
    db_type = st.selectbox(
        "Database Type",
        options=["SQLite", "PostgreSQL", "MySQL", "SQL Server"],
        help="Select your database management system"
    )
    
    # Connection form
    with st.form("database_connection"):
        col1, col2 = st.columns(2)
        
        with col1:
            if db_type == "SQLite":
                db_path = st.text_input("Database File Path", placeholder="/path/to/database.db")
                host = None
                port = None
                username = None
                password = None
                database = None
            else:
                host = st.text_input("Host", placeholder="localhost")
                port = st.number_input("Port", value=5432 if db_type == "PostgreSQL" else 3306)
                database = st.text_input("Database Name")
        
        with col2:
            if db_type != "SQLite":
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
            
            connection_name = st.text_input("Connection Name", value=f"{db_type} Connection")
        
        # Test query
        test_query = st.text_area(
            "Test Query (Optional)",
            placeholder="SELECT * FROM your_table LIMIT 10",
            help="Enter a query to test the connection"
        )
        
        submitted = st.form_submit_button("Connect Database", use_container_width=True)
        
        if submitted:
            # Connection validation (simplified for demo)
            if db_type == "SQLite" and db_path:
                try:
                    # Test SQLite connection
                    if os.path.exists(db_path):
                        st.success("✅ SQLite connection successful")
                        
                        source_config = {
                            'name': connection_name,
                            'type': f'{db_type} Database',
                            'status': 'Connected',
                            'host': db_path,
                            'connected_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            'test_query': test_query
                        }
                        
                        st.session_state.connected_sources.append(source_config)
                        st.rerun()
                    else:
                        st.error("❌ Database file not found")
                except Exception as e:
                    st.error(f"❌ Connection failed: {str(e)}")
            
            elif db_type != "SQLite" and host and database:
                # For demo purposes, we'll simulate the connection
                st.info("🔄 Connecting to database...")
                st.warning("⚠️ Database connections require actual credentials and network access")
                
                # Simulate connection status
                source_config = {
                    'name': connection_name,
                    'type': f'{db_type} Database',
                    'status': 'Connection Pending',
                    'host': host,
                    'port': port,
                    'database': database,
                    'connected_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'test_query': test_query
                }
                
                st.session_state.connected_sources.append(source_config)
                st.info("Connection configuration saved. Actual connection requires valid credentials.")
            
            else:
                st.error("❌ Please fill in all required fields")

def handle_api_connection():
    """Handle API endpoint connection"""
    st.header("🌐 API Endpoint")
    st.markdown("Connect to REST APIs for dynamic data retrieval")
    
    # API configuration form
    with st.form("api_connection"):
        col1, col2 = st.columns(2)
        
        with col1:
            api_url = st.text_input(
                "API Endpoint URL",
                placeholder="https://api.example.com/data"
            )
            
            method = st.selectbox(
                "HTTP Method",
                options=["GET", "POST"],
                index=0
            )
            
            connection_name = st.text_input(
                "Connection Name",
                value="API Connection"
            )
        
        with col2:
            # Headers
            st.subheader("Headers")
            auth_type = st.selectbox(
                "Authentication",
                options=["None", "API Key", "Bearer Token", "Basic Auth"]
            )
            
            if auth_type == "API Key":
                api_key_header = st.text_input("API Key Header", value="X-API-Key")
                api_key_value = st.text_input("API Key", type="password")
            elif auth_type == "Bearer Token":
                bearer_token = st.text_input("Bearer Token", type="password")
            elif auth_type == "Basic Auth":
                basic_username = st.text_input("Username")
                basic_password = st.text_input("Password", type="password")
        
        # Additional settings
        st.subheader("Settings")
        
        settings_col1, settings_col2 = st.columns(2)
        
        with settings_col1:
            refresh_interval = st.selectbox(
                "Refresh Interval",
                options=["Manual", "5 minutes", "15 minutes", "1 hour", "Daily"],
                index=0
            )
        
        with settings_col2:
            data_format = st.selectbox(
                "Response Format",
                options=["JSON", "CSV", "XML"],
                index=0
            )
        
        # Test endpoint
        test_endpoint = st.checkbox("Test endpoint on connection")
        
        submitted = st.form_submit_button("Connect API", use_container_width=True)
        
        if submitted:
            if api_url:
                # Simulate API connection (actual implementation would make HTTP request)
                st.info("🔄 Testing API connection...")
                
                # Build headers based on auth type
                headers = {}
                if auth_type == "API Key" and api_key_value:
                    headers[api_key_header] = api_key_value
                elif auth_type == "Bearer Token" and bearer_token:
                    headers["Authorization"] = f"Bearer {bearer_token}"
                
                source_config = {
                    'name': connection_name,
                    'type': 'API Endpoint',
                    'status': 'Connected',
                    'url': api_url,
                    'method': method,
                    'auth_type': auth_type,
                    'refresh_interval': refresh_interval,
                    'data_format': data_format,
                    'connected_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                st.session_state.connected_sources.append(source_config)
                st.success("✅ API connection configured successfully")
                st.info("Note: Actual API calls will be made when data is requested")
                st.rerun()
            else:
                st.error("❌ Please provide an API endpoint URL")

def handle_sample_data():
    """Handle sample data connections"""
    st.header("🎯 Sample Data")
    st.markdown("Use pre-built sample datasets for testing and demonstrations")
    
    # Display available sample datasets
    sample_datasets = st.session_state.sample_data
    
    for dataset_name, dataset_info in sample_datasets.items():
        with st.expander(f"📊 {dataset_name}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Description:** {dataset_info['description']}")
                st.write(f"**Records:** {len(dataset_info['data'])}")
                st.write(f"**Columns:** {len(dataset_info['data'].columns)}")
                
                # Show column names
                st.write("**Columns:**")
                for col in dataset_info['data'].columns:
                    st.write(f"  • {col}")
            
            with col2:
                st.write("**Data Preview:**")
                st.dataframe(dataset_info['data'].head(3))
            
            # Connect button
            if st.button(f"Connect {dataset_name}", key=f"connect_{dataset_name}"):
                source_config = {
                    'name': dataset_name,
                    'type': 'Sample Data',
                    'status': 'Connected',
                    'record_count': len(dataset_info['data']),
                    'columns': list(dataset_info['data'].columns),
                    'connected_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'data': dataset_info['data'],
                    'description': dataset_info['description']
                }
                
                st.session_state.connected_sources.append(source_config)
                st.success(f"✅ Connected to {dataset_name}")
                st.rerun()

def create_sample_datasets():
    """Create sample datasets for demonstration"""
    
    # Sales data
    sales_data = pd.DataFrame({
        'date': pd.date_range('2024-01-01', periods=100, freq='D'),
        'sales': np.random.normal(1000, 200, 100).astype(int),
        'region': np.random.choice(['North', 'South', 'East', 'West'], 100),
        'product': np.random.choice(['Product A', 'Product B', 'Product C'], 100),
        'customer_count': np.random.randint(10, 100, 100)
    })
    
    # Customer satisfaction data
    satisfaction_data = pd.DataFrame({
        'month': pd.date_range('2024-01-01', periods=12, freq='M'),
        'satisfaction_score': np.random.uniform(3.5, 5.0, 12),
        'response_count': np.random.randint(50, 200, 12),
        'department': np.random.choice(['Support', 'Sales', 'Product'], 12)
    })
    
    # Website analytics data
    analytics_data = pd.DataFrame({
        'date': pd.date_range('2024-01-01', periods=30, freq='D'),
        'page_views': np.random.randint(1000, 5000, 30),
        'unique_visitors': np.random.randint(500, 2000, 30),
        'bounce_rate': np.random.uniform(0.2, 0.8, 30),
        'conversion_rate': np.random.uniform(0.01, 0.1, 30)
    })
    
    return {
        'Sales Performance': {
            'data': sales_data,
            'description': 'Daily sales data with regional and product breakdowns'
        },
        'Customer Satisfaction': {
            'data': satisfaction_data,
            'description': 'Monthly customer satisfaction scores by department'
        },
        'Website Analytics': {
            'data': analytics_data,
            'description': 'Daily website traffic and conversion metrics'
        }
    }

if __name__ == "__main__":
    # Import numpy here to avoid issues if not available
    try:
        import numpy as np
    except ImportError:
        st.error("NumPy is required for sample data generation")
        st.stop()
    
    main()
