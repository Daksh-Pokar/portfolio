import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional

class DashboardComponents:
    """
    Utility class for rendering dashboard components and visualizations
    """
    
    def __init__(self):
        self.color_palette = [
            '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', 
            '#FECA57', '#FF9FF3', '#54A0FF', '#5F27CD'
        ]
    
    def render_chart(self, data: pd.DataFrame, chart_config: Dict[str, Any]) -> None:
        """
        Render a chart based on configuration
        
        Args:
            data: DataFrame containing the data
            chart_config: Dictionary with chart configuration
        """
        try:
            chart_type = chart_config.get('type', 'bar')
            title = chart_config.get('title', 'Chart')
            x_col = chart_config.get('x')
            y_col = chart_config.get('y')
            color_col = chart_config.get('color')
            
            # Create the appropriate chart
            if chart_type == 'line':
                fig = self._create_line_chart(data, x_col, y_col, color_col, title)
            elif chart_type == 'bar':
                fig = self._create_bar_chart(data, x_col, y_col, color_col, title)
            elif chart_type == 'scatter':
                fig = self._create_scatter_chart(data, x_col, y_col, color_col, title)
            elif chart_type == 'histogram':
                fig = self._create_histogram(data, x_col, title)
            elif chart_type == 'box':
                fig = self._create_box_plot(data, x_col, y_col, color_col, title)
            elif chart_type == 'pie':
                fig = self._create_pie_chart(data, x_col, title)
            else:
                st.error(f"Unsupported chart type: {chart_type}")
                return
            
            # Display the chart
            st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error rendering chart '{title}': {str(e)}")
    
    def _create_line_chart(
        self, 
        data: pd.DataFrame, 
        x_col: str, 
        y_col: str, 
        color_col: Optional[str], 
        title: str
    ) -> go.Figure:
        """Create a line chart"""
        
        if color_col and color_col in data.columns:
            fig = px.line(
                data, 
                x=x_col, 
                y=y_col, 
                color=color_col,
                title=title,
                color_discrete_sequence=self.color_palette
            )
        else:
            fig = px.line(
                data, 
                x=x_col, 
                y=y_col,
                title=title,
                color_discrete_sequence=self.color_palette
            )
        
        fig.update_layout(
            title_font_size=16,
            xaxis_title=x_col.replace('_', ' ').title(),
            yaxis_title=y_col.replace('_', ' ').title() if y_col else '',
            showlegend=True if color_col else False
        )
        
        return fig
    
    def _create_bar_chart(
        self, 
        data: pd.DataFrame, 
        x_col: str, 
        y_col: str, 
        color_col: Optional[str], 
        title: str
    ) -> go.Figure:
        """Create a bar chart"""
        
        if color_col and color_col in data.columns:
            fig = px.bar(
                data, 
                x=x_col, 
                y=y_col, 
                color=color_col,
                title=title,
                color_discrete_sequence=self.color_palette
            )
        else:
            fig = px.bar(
                data, 
                x=x_col, 
                y=y_col,
                title=title,
                color_discrete_sequence=self.color_palette
            )
        
        fig.update_layout(
            title_font_size=16,
            xaxis_title=x_col.replace('_', ' ').title(),
            yaxis_title=y_col.replace('_', ' ').title() if y_col else '',
            showlegend=True if color_col else False
        )
        
        return fig
    
    def _create_scatter_chart(
        self, 
        data: pd.DataFrame, 
        x_col: str, 
        y_col: str, 
        color_col: Optional[str], 
        title: str
    ) -> go.Figure:
        """Create a scatter plot"""
        
        if color_col and color_col in data.columns:
            fig = px.scatter(
                data, 
                x=x_col, 
                y=y_col, 
                color=color_col,
                title=title,
                color_discrete_sequence=self.color_palette
            )
        else:
            fig = px.scatter(
                data, 
                x=x_col, 
                y=y_col,
                title=title,
                color_discrete_sequence=self.color_palette
            )
        
        fig.update_layout(
            title_font_size=16,
            xaxis_title=x_col.replace('_', ' ').title(),
            yaxis_title=y_col.replace('_', ' ').title() if y_col else ''
        )
        
        return fig
    
    def _create_histogram(
        self, 
        data: pd.DataFrame, 
        x_col: str, 
        title: str
    ) -> go.Figure:
        """Create a histogram"""
        
        fig = px.histogram(
            data, 
            x=x_col,
            title=title,
            color_discrete_sequence=self.color_palette
        )
        
        fig.update_layout(
            title_font_size=16,
            xaxis_title=x_col.replace('_', ' ').title(),
            yaxis_title='Count'
        )
        
        return fig
    
    def _create_box_plot(
        self, 
        data: pd.DataFrame, 
        x_col: str, 
        y_col: str, 
        color_col: Optional[str], 
        title: str
    ) -> go.Figure:
        """Create a box plot"""
        
        if color_col and color_col in data.columns:
            fig = px.box(
                data, 
                x=x_col, 
                y=y_col, 
                color=color_col,
                title=title,
                color_discrete_sequence=self.color_palette
            )
        else:
            fig = px.box(
                data, 
                x=x_col, 
                y=y_col,
                title=title,
                color_discrete_sequence=self.color_palette
            )
        
        fig.update_layout(
            title_font_size=16,
            xaxis_title=x_col.replace('_', ' ').title(),
            yaxis_title=y_col.replace('_', ' ').title() if y_col else ''
        )
        
        return fig
    
    def _create_pie_chart(
        self, 
        data: pd.DataFrame, 
        values_col: str, 
        title: str
    ) -> go.Figure:
        """Create a pie chart"""
        
        # Aggregate data for pie chart
        if data[values_col].dtype in ['object', 'category']:
            # For categorical data, count occurrences
            pie_data = data[values_col].value_counts()
        else:
            # For numeric data, group by unique values and sum
            pie_data = data.groupby(values_col).size()
        
        fig = px.pie(
            values=pie_data.values,
            names=pie_data.index,
            title=title,
            color_discrete_sequence=self.color_palette
        )
        
        fig.update_layout(
            title_font_size=16
        )
        
        return fig
    
    def render_metric_card(
        self, 
        title: str, 
        value: Any, 
        delta: Optional[Any] = None,
        help_text: Optional[str] = None
    ) -> None:
        """Render a metric card component"""
        
        st.metric(
            label=title,
            value=value,
            delta=delta,
            help=help_text
        )
    
    def render_kpi_grid(self, metrics: Dict[str, Dict[str, Any]]) -> None:
        """
        Render a grid of KPI metrics
        
        Args:
            metrics: Dictionary of metric configurations
                    Format: {'metric_name': {'value': ..., 'delta': ..., 'help': ...}}
        """
        
        # Create columns based on number of metrics
        num_metrics = len(metrics)
        cols = st.columns(num_metrics)
        
        for i, (metric_name, metric_config) in enumerate(metrics.items()):
            with cols[i]:
                self.render_metric_card(
                    title=metric_name,
                    value=metric_config.get('value', 'N/A'),
                    delta=metric_config.get('delta'),
                    help_text=metric_config.get('help')
                )
    
    def render_data_table(
        self, 
        data: pd.DataFrame, 
        title: Optional[str] = None,
        max_rows: int = 100
    ) -> None:
        """Render a data table with optional title"""
        
        if title:
            st.subheader(title)
        
        # Limit rows for performance
        display_data = data.head(max_rows) if len(data) > max_rows else data
        
        st.dataframe(display_data, use_container_width=True)
        
        if len(data) > max_rows:
            st.info(f"Showing first {max_rows} rows out of {len(data)} total rows")
    
    def render_filter_sidebar(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Render filter controls in sidebar
        
        Args:
            data: DataFrame to create filters for
            
        Returns:
            Dict: Applied filters
        """
        
        filters = {}
        
        st.sidebar.header("Filters")
        
        # Numeric filters
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if data[col].nunique() > 1:  # Only create filter if there's variation
                min_val = float(data[col].min())
                max_val = float(data[col].max())
                
                if min_val != max_val:
                    selected_range = st.sidebar.slider(
                        f"{col.replace('_', ' ').title()}",
                        min_value=min_val,
                        max_value=max_val,
                        value=(min_val, max_val),
                        key=f"filter_{col}"
                    )
                    filters[col] = selected_range
        
        # Categorical filters
        categorical_cols = data.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            unique_vals = data[col].dropna().unique()
            if len(unique_vals) > 1 and len(unique_vals) <= 20:  # Reasonable number of options
                selected_vals = st.sidebar.multiselect(
                    f"{col.replace('_', ' ').title()}",
                    options=unique_vals,
                    default=unique_vals,
                    key=f"filter_{col}"
                )
                if len(selected_vals) < len(unique_vals):
                    filters[col] = selected_vals
        
        return filters
    
    def apply_filters(self, data: pd.DataFrame, filters: Dict[str, Any]) -> pd.DataFrame:
        """Apply filters to data"""
        
        filtered_data = data.copy()
        
        for col, filter_value in filters.items():
            if col in data.columns:
                if isinstance(filter_value, (list, tuple)) and len(filter_value) == 2:
                    # Range filter for numeric data
                    filtered_data = filtered_data[
                        (filtered_data[col] >= filter_value[0]) & 
                        (filtered_data[col] <= filter_value[1])
                    ]
                elif isinstance(filter_value, list):
                    # Multi-select filter for categorical data
                    filtered_data = filtered_data[filtered_data[col].isin(filter_value)]
        
        return filtered_data
    
    def render_summary_stats(self, data: pd.DataFrame) -> None:
        """Render summary statistics for the dataset"""
        
        st.subheader("Dataset Summary")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Rows", len(data))
        
        with col2:
            st.metric("Total Columns", len(data.columns))
        
        with col3:
            missing_count = data.isnull().sum().sum()
            st.metric("Missing Values", missing_count)
        
        # Detailed statistics
        if st.checkbox("Show Detailed Statistics"):
            numeric_data = data.select_dtypes(include=[np.number])
            if not numeric_data.empty:
                st.subheader("Numeric Column Statistics")
                st.dataframe(numeric_data.describe())
            
            categorical_data = data.select_dtypes(include=['object'])
            if not categorical_data.empty:
                st.subheader("Categorical Column Info")
                cat_summary = pd.DataFrame({
                    'Column': categorical_data.columns,
                    'Unique Values': [categorical_data[col].nunique() for col in categorical_data.columns],
                    'Most Frequent': [categorical_data[col].mode().iloc[0] if not categorical_data[col].mode().empty else 'N/A' for col in categorical_data.columns]
                })
                st.dataframe(cat_summary)
