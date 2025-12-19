import pandas as pd
from db import run_query 


def load_case_metadata() -> pd.DataFrame:
    """
    Loads static metadata for case studies (IDs, titles, descriptions).
    Assumes a 'case_metadata' table exists.
    """
    sql = """
        SELECT case_id, title, description
        FROM case_metadata
        ORDER BY case_id;
    """
    return run_query(sql)
