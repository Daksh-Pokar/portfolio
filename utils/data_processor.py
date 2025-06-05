import pandas as pd
import json
import io
from typing import Union, Dict, Any
import streamlit as st

class DataProcessor:
    """
    Utility class for processing various data formats and sources
    """
    
    def __init__(self):
        self.supported_formats = ['.csv', '.xlsx', '.json']
    
    def load_file(self, uploaded_file) -> pd.DataFrame:
        """
        Load data from an uploaded file
        
        Args:
            uploaded_file: Streamlit uploaded file object
            
        Returns:
            pd.DataFrame: Processed data
            
        Raises:
            ValueError: If file format is not supported
            Exception: If file processing fails
        """
        try:
            file_extension = self._get_file_extension(uploaded_file.name)
            
            if file_extension == '.csv':
                return self._load_csv(uploaded_file)
            elif file_extension == '.xlsx':
                return self._load_excel(uploaded_file)
            elif file_extension == '.json':
                return self._load_json(uploaded_file)
            else:
                raise ValueError(f"Unsupported file format: {file_extension}")
                
        except Exception as e:
            raise Exception(f"Error processing file: {str(e)}")
    
    def _get_file_extension(self, filename: str) -> str:
        """Extract file extension from filename"""
        return '.' + filename.split('.')[-1].lower()
    
    def _load_csv(self, uploaded_file) -> pd.DataFrame:
        """Load CSV file with automatic delimiter detection"""
        try:
            # Try common delimiters
            content = uploaded_file.getvalue().decode('utf-8')
            
            # Try to detect delimiter
            if '\t' in content[:1000]:
                delimiter = '\t'
            elif ';' in content[:1000]:
                delimiter = ';'
            else:
                delimiter = ','
            
            # Reset file pointer
            uploaded_file.seek(0)
            
            df = pd.read_csv(uploaded_file, delimiter=delimiter)
            
            # Clean column names
            df.columns = df.columns.str.strip()
            
            return df
            
        except Exception as e:
            raise Exception(f"Error reading CSV file: {str(e)}")
    
    def _load_excel(self, uploaded_file) -> pd.DataFrame:
        """Load Excel file"""
        try:
            # Read all sheets and let user choose if multiple
            excel_file = pd.ExcelFile(uploaded_file)
            
            if len(excel_file.sheet_names) > 1:
                # For simplicity, use the first sheet
                # In a full implementation, you'd let user choose
                sheet_name = excel_file.sheet_names[0]
                st.info(f"Multiple sheets found. Using sheet: {sheet_name}")
            else:
                sheet_name = excel_file.sheet_names[0]
            
            df = pd.read_excel(uploaded_file, sheet_name=sheet_name)
            
            # Clean column names
            df.columns = df.columns.str.strip()
            
            return df
            
        except Exception as e:
            raise Exception(f"Error reading Excel file: {str(e)}")
    
    def _load_json(self, uploaded_file) -> pd.DataFrame:
        """Load JSON file"""
        try:
            content = uploaded_file.getvalue().decode('utf-8')
            json_data = json.loads(content)
            
            # Handle different JSON structures
            if isinstance(json_data, list):
                # List of objects
                df = pd.DataFrame(json_data)
            elif isinstance(json_data, dict):
                # Dictionary - try to convert to DataFrame
                if all(isinstance(v, (list, tuple)) for v in json_data.values()):
                    # Dictionary of lists
                    df = pd.DataFrame(json_data)
                else:
                    # Single record or nested structure
                    df = pd.json_normalize(json_data)
            else:
                raise ValueError("JSON structure not supported")
            
            return df
            
        except Exception as e:
            raise Exception(f"Error reading JSON file: {str(e)}")
    
    def clean_data(self, df: pd.DataFrame, options: Dict[str, Any] = None) -> pd.DataFrame:
        """
        Clean and preprocess data
        
        Args:
            df: Input DataFrame
            options: Cleaning options
            
        Returns:
            pd.DataFrame: Cleaned data
        """
        if options is None:
            options = {}
        
        cleaned_df = df.copy()
        
        # Remove completely empty rows and columns
        if options.get('remove_empty', True):
            cleaned_df = cleaned_df.dropna(how='all')  # Remove empty rows
            cleaned_df = cleaned_df.dropna(axis=1, how='all')  # Remove empty columns
        
        # Convert data types
        if options.get('auto_convert_types', True):
            cleaned_df = self._auto_convert_types(cleaned_df)
        
        # Handle duplicates
        if options.get('remove_duplicates', False):
            cleaned_df = cleaned_df.drop_duplicates()
        
        # Strip whitespace from string columns
        if options.get('strip_whitespace', True):
            string_columns = cleaned_df.select_dtypes(include=['object']).columns
            for col in string_columns:
                if cleaned_df[col].dtype == 'object':
                    cleaned_df[col] = cleaned_df[col].astype(str).str.strip()
        
        return cleaned_df
    
    def _auto_convert_types(self, df: pd.DataFrame) -> pd.DataFrame:
        """Automatically convert column types"""
        converted_df = df.copy()
        
        for column in converted_df.columns:
            # Try to convert to numeric
            if converted_df[column].dtype == 'object':
                try:
                    # Try to convert to datetime first
                    if self._looks_like_date(converted_df[column]):
                        converted_df[column] = pd.to_datetime(converted_df[column], errors='ignore')
                    else:
                        # Try numeric conversion
                        converted_df[column] = pd.to_numeric(converted_df[column], errors='ignore')
                except:
                    # Keep as string if conversion fails
                    pass
        
        return converted_df
    
    def _looks_like_date(self, series: pd.Series) -> bool:
        """Check if a series looks like it contains dates"""
        # Sample a few non-null values
        sample = series.dropna().head(10)
        
        if len(sample) == 0:
            return False
        
        # Check if values contain date-like patterns
        date_patterns = ['-', '/', ':', 'T', ' ']
        
        for value in sample:
            value_str = str(value)
            if len(value_str) > 6 and any(pattern in value_str for pattern in date_patterns):
                # Try to parse one value
                try:
                    pd.to_datetime(value_str)
                    return True
                except:
                    continue
        
        return False
    
    def get_data_summary(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate a comprehensive summary of the dataset
        
        Args:
            df: Input DataFrame
            
        Returns:
            Dict: Data summary information
        """
        summary = {
            'shape': df.shape,
            'columns': list(df.columns),
            'dtypes': df.dtypes.to_dict(),
            'missing_values': df.isnull().sum().to_dict(),
            'memory_usage': df.memory_usage(deep=True).sum(),
            'numeric_columns': list(df.select_dtypes(include=['number']).columns),
            'categorical_columns': list(df.select_dtypes(include=['object']).columns),
            'datetime_columns': list(df.select_dtypes(include=['datetime']).columns)
        }
        
        # Add basic statistics for numeric columns
        if summary['numeric_columns']:
            summary['numeric_stats'] = df[summary['numeric_columns']].describe().to_dict()
        
        # Add unique value counts for categorical columns
        if summary['categorical_columns']:
            summary['categorical_stats'] = {}
            for col in summary['categorical_columns']:
                if len(df[col].unique()) <= 20:  # Only for columns with reasonable number of unique values
                    summary['categorical_stats'][col] = df[col].value_counts().to_dict()
        
        return summary
    
    def validate_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Validate data quality and identify potential issues
        
        Args:
            df: Input DataFrame
            
        Returns:
            Dict: Validation results
        """
        validation_results = {
            'is_valid': True,
            'warnings': [],
            'errors': [],
            'recommendations': []
        }
        
        # Check for empty dataset
        if df.empty:
            validation_results['errors'].append("Dataset is empty")
            validation_results['is_valid'] = False
            return validation_results
        
        # Check for missing data
        missing_percentage = (df.isnull().sum() / len(df)) * 100
        high_missing_cols = missing_percentage[missing_percentage > 50].index.tolist()
        
        if high_missing_cols:
            validation_results['warnings'].append(
                f"Columns with >50% missing data: {high_missing_cols}"
            )
        
        # Check for duplicate rows
        duplicate_count = df.duplicated().sum()
        if duplicate_count > 0:
            validation_results['warnings'].append(
                f"Found {duplicate_count} duplicate rows"
            )
        
        # Check for constant columns
        constant_cols = []
        for col in df.columns:
            if df[col].nunique() <= 1:
                constant_cols.append(col)
        
        if constant_cols:
            validation_results['warnings'].append(
                f"Constant columns (single value): {constant_cols}"
            )
        
        # Recommendations
        if len(df.columns) > 50:
            validation_results['recommendations'].append(
                "Consider selecting relevant columns for better performance"
            )
        
        if len(df) > 100000:
            validation_results['recommendations'].append(
                "Large dataset detected. Consider sampling for initial analysis"
            )
        
        return validation_results
