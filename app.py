import pandas as pd 
import streamlit as st 
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

import utils.db_utils as db

#1 Initial configuration
st.set_page_config(page_title='Real Estate Data', page_icon=':house_with_garden:', layout="wide")
st.title('Real Estate Data')

#2 Add features to sidebar:
add_selectbox = st.sidebar.selectbox(
    'Select Dataset',
    ('Absentee Owners','Master Data')
)

#3 Pull list data
absentee_owner_list_df = db.read_sql_from_bigQuery('SELECT * FROM canvas-antler-390503.DataLists.AbsenteeOwners LIMIT 1000')

#4 Display dataframes
## Absentee owner list
st.header('Absentee Owners List')
absentee_grid_table = AgGrid(absentee_owner_list_df, 
        height=500,
        width=1000
        )