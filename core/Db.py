"""
BigQuery database connection and query helpers
Uses google-cloud-bigquery client with service account authentication
"""

import streamlit as st
from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd
from typing import Optional
from core.settings import BIGQUERY_CONFIG, get_table_ref

@st.cache_resource
def get_bigquery_client():
    """
    Initialize and cache BigQuery client using service account from secrets
    
    Returns:
        bigquery.Client instance
    """
    try:
        # Get service account credentials from Streamlit secrets
        credentials = service_account.Credentials.from_service_account_info(
            st.secrets["gcp_service_account"]
        )
        
        # Create BigQuery client
        client = bigquery.Client(
            credentials=credentials,
            project=BIGQUERY_CONFIG['project_id'],
            location=BIGQUERY_CONFIG['location']
        )
        
        return client
    
    except Exception as e:
        st.error(f"❌ Failed to initialize BigQuery client: {str(e)}")
        st.info("Please ensure your secrets are configured correctly in Streamlit Cloud.")
        return None

@st.cache_data(ttl=300)
def run_query(query: str, _client: Optional[bigquery.Client] = None) -> Optional[pd.DataFrame]:
    """
    Execute a BigQuery SQL query and return results as DataFrame
    
    Args:
        query: SQL query string
        _client: BigQuery client (will be initialized if None)
    
    Returns:
        pandas DataFrame with query results, or None on error
    """
    try:
        if _client is None:
            _client = get_bigquery_client()
        
        if _client is None:
            return None
        
        # Run query
        query_job = _client.query(query)
        results = query_job.result()
        
        # Convert to DataFrame
        df = results.to_dataframe()
        
        return df
    
    except Exception as e:
        st.error(f"❌ Query execution error: {str(e)}")
        with st.expander("View Query"):
            st.code(query, language="sql")
        return None

def test_connection() -> tuple:
    """
    Test BigQuery connection and return status
    
    Returns:
        Tuple of (success: bool, message: str)
    """
    try:
        client = get_bigquery_client()
        
        if client is None:
            return False, "Failed to initialize client"
        
        # Try a simple query
        test_query = f"""
        SELECT COUNT(*) as count 
        FROM {get_table_ref('user')}
        LIMIT 1
        """
        
        result = run_query(test_query, client)
        
        if result is not None:
            return True, "Connection successful"
        else:
            return False, "Query execution failed"
    
    except Exception as e:
        return False, f"Connection test failed: {str(e)}"

def check_table_exists(table_name: str, _client: Optional[bigquery.Client] = None) -> bool:
    """
    Check if a table exists in the dataset
    
    Args:
        table_name: Name of the table to check
        _client: BigQuery client
    
    Returns:
        True if table exists, False otherwise
    """
    try:
        if _client is None:
            _client = get_bigquery_client()
        
        if _client is None:
            return False
        
        table_ref = f"{BIGQUERY_CONFIG['project_id']}.{BIGQUERY_CONFIG['dataset']}.{table_name}"
        
        # Try to get table metadata
        _client.get_table(table_ref)
        return True
    
    except Exception:
        return False

def get_table_schema(table_name: str, _client: Optional[bigquery.Client] = None) -> Optional[list]:
    """
    Get schema information for a table
    
    Args:
        table_name: Name of the table
        _client: BigQuery client
    
    Returns:
        List of schema fields or None
    """
    try:
        if _client is None:
            _client = get_bigquery_client()
        
        if _client is None:
            return None
        
        table_ref = f"{BIGQUERY_CONFIG['project_id']}.{BIGQUERY_CONFIG['dataset']}.{table_name}"
        table = _client.get_table(table_ref)
        
        return [
            {
                'name': field.name,
                'type': field.field_type,
                'mode': field.mode
            }
            for field in table.schema
        ]
    
    except Exception as e:
        st.warning(f"Could not fetch schema for {table_name}: {str(e)}")
        return None

@st.cache_data(ttl=3600)
def get_available_tables(_client: Optional[bigquery.Client] = None) -> list:
    """
    Get list of available tables in the dataset
    
    Args:
        _client: BigQuery client
    
    Returns:
        List of table names
    """
    try:
        if _client is None:
            _client = get_bigquery_client()
        
        if _client is None:
            return []
        
        dataset_ref = f"{BIGQUERY_CONFIG['project_id']}.{BIGQUERY_CONFIG['dataset']}"
        tables = _client.list_tables(dataset_ref)
        
        return [table.table_id for table in tables]
    
    except Exception as e:
        st.warning(f"Could not list tables: {str(e)}")
        return []
