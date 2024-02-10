import pandas as pd

from google.cloud import bigquery
from google.cloud.bigquery import dbapi

CREDS = 'real-estate-data-processing-dbfdca2ea196.json'
PROJECT_ID = 'real-estate-data-processing'

def get_bigQuery_client():
    """
    Description: Return client connection from BigQuery. Client is needed to run jobs and get SQL cursor connection.
    Args: None
    Returns: 
        bigquery.Client(): BigQuery client connection
    """
    return bigquery.Client.from_service_account_json(json_credentials_path=CREDS)

def get_bigQuery_connection():
    """
    Description: Return connection from BigQuery, used for executing cursor SQL code
    Args: None
    Returns: 
        conn: BigQuery SQL connection
    """
    client = get_bigQuery_client()
    conn = dbapi.Connection(client)
    return conn

def read_sql_from_bigQuery(sql:str, project_id: str):
    client = get_bigQuery_client()
    df = client.query(sql, project=project_id).to_dataframe()
    df = df.fillna(value=pd.NA)
    return df