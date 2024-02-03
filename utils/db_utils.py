import pandas as pd
from pathlib import Path 
import os

from google.cloud import bigquery
from google.cloud.bigquery import dbapi
import pandas_gbq

def connect_bigQuery_credentials(json_name: str = 'pythonbq.privateKey.json'):
    """
    Description: Establishes the GCP credentials path in order to make GCP API client connections
    Args: 
        json_name: The string name of the GCP private key json in main working directory
    Returns: None
    """
    credentials_path = str(Path.cwd() / 'pythonbq.privateKey.json')
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path

def get_bigQuery_client():
    """
    Description: Return client connection from BigQuery. Client is needed to run jobs and get SQL cursor connection.
    Args: None
    Returns: 
        bigquery.Client(): BigQuery client connection
    """
    return bigquery.Client(project='canvas-antler-390503')

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


def read_sql_from_bigQuery(sql:str, proj_id: str = 'canvas-antler-390503'):
    df = pandas_gbq.read_gbq(sql, project_id=proj_id, progress_bar_type=None)
    return df