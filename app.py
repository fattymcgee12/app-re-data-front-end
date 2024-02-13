import pandas as pd 

from google.cloud import bigquery

import streamlit as st 
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

import utils.common_utils as utils
import utils.db_utils as db

#1 Variables
project_id = "real-estate-data-processing"

#2 Initial configuration
st.set_page_config(page_title='Real Estate Data', page_icon=':house_with_garden:', layout="wide")
st.title('Real Estate Data')

## Add dataset select to sidebar
dataset_select = st.sidebar.selectbox(
    'Select Dataset',
    ('Absentee Owners','Master Data')
)

## If absentee owner is selected
if dataset_select == 'Absentee Owners':
    ## Create city selection
    city_list = db.read_sql_from_bigQuery('SELECT DISTINCT City FROM `real-estate-data-processing.DataLists.AbsenteeOwners` ORDER BY City asc', project_id)
    city_list = city_list['City'].values.tolist()
    city_select = st.sidebar.multiselect(label='City:', options=city_list, default=city_list[0])

    ## Put selections in query
    dataset_sql = f"""
            SELECT * 
            FROM real-estate-data-processing.DataLists.AbsenteeOwners 
            WHERE City {utils.list_to_in_phrase(city_select)}
        """
    
## Query and display absentee owner data with selections
display_df = db.read_sql_from_bigQuery(dataset_sql, project_id)

#5 Display dataframe
go_builder = GridOptionsBuilder.from_dataframe(display_df)
go_builder.configure_grid_options(alwaysShowHorizontalScroll=True)
go_builder.configure_pagination(enabled=True, paginationAutoPageSize=False, paginationPageSize=25)
go = go_builder.build()

agdf = AgGrid(display_df, gridOptions=go, theme='streamlit')