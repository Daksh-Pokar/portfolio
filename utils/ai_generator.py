import os
import pandas as pd
from typing import Optional, Dict, Any
import json

class AIGenerator:
    """
    AI-powered report and insight generator
    Uses OpenAI's API for generating intelligent data analysis reports
    """
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = "gpt-3.5-turbo"
        self.max_tokens = 2000
        
    def is_available(self) -> bool:
        """Check if AI services are available"""
        return self.api_key is not None and self.api_key.strip() != ""
    
    def generate_report(
        self, 
        data: pd.DataFrame, 
        query: str, 
        report_type: str = "Data Summary",
        depth: str = "Standard",
        include_visualizations: bool = True
    ) -> Optional[str]:
        """
        Generate an AI-powered data analysis report
        
        Args:
            data: The dataset to analyze
            query: Specific question or analysis request
            report_type: Type of report to generate
            depth: Analysis depth (Quick, Standard, Detailed)
            include_visualizations: Whether to include visualization suggestions
            
        Returns:
            str: Generated report content or None if failed
        """
        if not self.is_available():
            return None
            
        try:
            # Prepare data summary for AI context
            data_context = self._prepare_data_context(data)
            
            # Build the prompt
            prompt = self._build_analysis_prompt(
                data_context, query, report_type, depth, include_visualizations
            )
            
            # Make API call
            report_content = self._call_openai_api(prompt)
            
            return report_content
            
        except Exception as e:
            print(f"Error generating AI report: {str(e)}")
            return None
    
    def _prepare_data_context(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Prepare data context for AI analysis"""
        
        # Basic dataset information
        context = {
            'shape': data.shape,
            'columns': list(data.columns),
            'dtypes': data.dtypes.astype(str).to_dict()
        }
        
        # Sample data (first few rows)
        context['sample_data'] = data.head(3).to_dict('records')
        
        # Basic statistics for numeric columns
        numeric_cols = data.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            context['numeric_summary'] = data[numeric_cols].describe().to_dict()
        
        # Categorical column information
        categorical_cols = data.select_dtypes(include=['object']).columns
        if len(categorical_cols) > 0:
            context['categorical_info'] = {}
            for col in categorical_cols:
                unique_count = data[col].nunique()
                if unique_count <= 10:  # Only show values for columns with few unique values
                    context['categorical_info'][col] = {
                        'unique_count': unique_count,
                        'top_values': data[col].value_counts().head(5).to_dict()
                    }
                else:
                    context['categorical_info'][col] = {
                        'unique_count': unique_count,
                        'sample_values': data[col].dropna().unique()[:5].tolist()
                    }
        
        # Missing data information
        missing_data = data.isnull().sum()
        if missing_data.sum() > 0:
            context['missing_data'] = missing_data[missing_data > 0].to_dict()
        
        return context
    
    def _build_analysis_prompt(
        self,
        data_context: Dict[str, Any],
        query: str,
        report_type: str,
        depth: str,
        include_visualizations: bool
    ) -> str:
        """Build the analysis prompt for the AI model"""
        
        prompt = f"""
You are a professional data analyst. Analyze the provided dataset and answer the user's question with detailed insights.

DATASET INFORMATION:
- Shape: {data_context['shape']} (rows, columns)
- Columns: {', '.join(data_context['columns'])}
- Data Types: {json.dumps(data_context['dtypes'], indent=2)}

SAMPLE DATA:
{json.dumps(data_context['sample_data'], indent=2)}
"""
        
        # Add numeric summary if available
        if 'numeric_summary' in data_context:
            prompt += f"\nNUMERIC COLUMN STATISTICS:\n{json.dumps(data_context['numeric_summary'], indent=2)}"
        
        # Add categorical information if available
        if 'categorical_info' in data_context:
            prompt += f"\nCATEGORICAL COLUMN INFO:\n{json.dumps(data_context['categorical_info'], indent=2)}"
        
        # Add missing data information if available
        if 'missing_data' in data_context:
            prompt += f"\nMISSING DATA:\n{json.dumps(data_context['missing_data'], indent=2)}"
        
        # Add analysis requirements
        prompt += f"""

ANALYSIS REQUEST:
{query}

REPORT TYPE: {report_type}
ANALYSIS DEPTH: {depth}

REQUIREMENTS:
1. Provide a {depth.lower()} analysis based on the data shown above
2. Focus on answering the specific question: "{query}"
3. Include key findings, patterns, and insights
4. Highlight any notable trends or anomalies
5. Provide actionable recommendations based on the data
"""
        
        if depth == "Detailed":
            prompt += "6. Include statistical significance where relevant\n7. Discuss potential limitations and data quality considerations\n"
        
        if include_visualizations:
            prompt += """8. Suggest appropriate visualizations that would help illustrate your findings
9. Recommend specific chart types and what variables to plot
"""
        
        prompt += """
FORMAT YOUR RESPONSE:
- Use clear headings and bullet points
- Include specific numbers and percentages from the data
- Write in a professional, analytical tone
- Make insights actionable and business-relevant
"""
        
        return prompt
    
    def _call_openai_api(self, prompt: str) -> Optional[str]:
        """Make API call to OpenAI"""
        try:
            import openai
            
            # Set up the client
            client = openai.OpenAI(api_key=self.api_key)
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a professional data analyst with expertise in statistical analysis, data visualization, and business intelligence. Provide clear, actionable insights based on data."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                max_tokens=self.max_tokens,
                temperature=0.3  # Lower temperature for more consistent, factual responses
            )
            
            return response.choices[0].message.content
            
        except ImportError:
            return "OpenAI library not available. Please install: pip install openai"
        except Exception as e:
            return f"Error calling OpenAI API: {str(e)}"
    
    def generate_chart_suggestions(self, data: pd.DataFrame, analysis_goal: str) -> Optional[str]:
        """Generate specific chart and visualization suggestions"""
        
        if not self.is_available():
            return None
        
        data_context = self._prepare_data_context(data)
        
        prompt = f"""
Based on the following dataset, suggest the most appropriate charts and visualizations for the analysis goal: "{analysis_goal}"

DATASET INFO:
- Shape: {data_context['shape']}
- Columns: {', '.join(data_context['columns'])}
- Data Types: {json.dumps(data_context['dtypes'], indent=2)}
"""
        
        if 'numeric_summary' in data_context:
            prompt += f"\nNumeric columns: {list(data_context['numeric_summary'].keys())}"
        
        if 'categorical_info' in data_context:
            prompt += f"\nCategorical columns: {list(data_context['categorical_info'].keys())}"
        
        prompt += """

Provide specific recommendations for:
1. Chart types (bar, line, scatter, histogram, box plot, heatmap, etc.)
2. Which variables to use for X and Y axes
3. Color coding suggestions
4. Any filtering or grouping recommendations
5. Dashboard layout suggestions

Format as a practical, actionable list.
"""
        
        return self._call_openai_api(prompt)
    
    def generate_insight_summary(self, data: pd.DataFrame) -> Optional[str]:
        """Generate a quick insight summary of the dataset"""
        
        if not self.is_available():
            return None
        
        data_context = self._prepare_data_context(data)
        
        prompt = f"""
Provide a concise summary of key insights from this dataset:

DATASET:
- Shape: {data_context['shape']}
- Columns: {', '.join(data_context['columns'])}
- Sample: {json.dumps(data_context['sample_data'], indent=2)}

Focus on:
1. Most important patterns or trends
2. Notable outliers or anomalies
3. Data quality observations
4. 2-3 key business insights

Keep it under 300 words and actionable.
"""
        
        return self._call_openai_api(prompt)
