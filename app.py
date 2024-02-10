import pandas as pd 

from google.cloud import bigquery

import streamlit as st 
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

import utils.db_utils as db

#1 Variables
CREDS = 'real-estate-data-processing-dbfdca2ea196.json'
project_id = "real-estate-data-processing"

#2 Initial configuration
st.set_page_config(page_title='Real Estate Data', page_icon=':house_with_garden:', layout="wide")
st.title('Real Estate Data')

#3 Add features to sidebar:
add_selectbox = st.sidebar.selectbox(
    'Select Dataset',
    ('Absentee Owners','Master Data')
)

#4 Pull list data

## Run a query using a Service Account json credentials connection
client = bigquery.Client.from_service_account_json(json_credentials_path=CREDS)
sql = """
    SELECT * FROM real-estate-data-processing.DataLists.AbsenteeOwners LIMIT 1000
"""

absentee_owner_list_df = db.read_sql_from_bigQuery(sql, project_id)

#5 Display dataframes
## Absentee owner list
st.header('Absentee Owners List')
absentee_grid_table = AgGrid(absentee_owner_list_df, 
        height=500,
        width=1000
        )