import pandas as pd 
import numpy as np
import plotly.express as px

from google.cloud import bigquery

import streamlit as st 
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

import utils.common_utils as utils
import utils.db_utils as db

def display_map(location_data):
    fig = px.scatter_mapbox(location_data, lat='LAT', lon='LON', hover_name='Address', hover_data=['BuildingDescription', 'SF', 'AssessedValue'],zoom=10, size=location_data['SF'].astype('int'), color=location_data['SF'].astype('int'), color_continuous_scale=px.colors.cyclical.IceFire, height=750)
    fig.update_layout(mapbox_style='carto-positron')
    return fig

# size=np.array(location_data.AssessedValue).astype(int)

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

    ## Query selections for data table
    dataset_sql = f"""
            SELECT * 
            FROM real-estate-data-processing.DataLists.AbsenteeOwners 
            WHERE City {utils.list_to_in_phrase(city_select)}
        """
    
    ## Columns to be displayed in table
    display_cols = ['Address','City','County','State','OwnerName','OwnerAddress','OwnerCity','OwnerState','OwnerZip','BuildingDescription','SF','Bedrooms','Bathrooms','YearBuilt','AssessedValue','LastSalesPrice','LastSalesDate']
    
## Query data with selections
main_df = db.read_sql_from_bigQuery(dataset_sql, project_id)

## Display map with properties in dataframe
px_map = display_map(main_df)
st.plotly_chart(px_map, use_container_width=True)

## Display dataframe
## Filter dataframe with display columns
go_builder = GridOptionsBuilder.from_dataframe(main_df[display_cols])
go_builder.configure_grid_options(alwaysShowHorizontalScroll=True)
go_builder.configure_pagination(enabled=True, paginationAutoPageSize=False, paginationPageSize=25)
go = go_builder.build()

agdf = AgGrid(main_df[display_cols], gridOptions=go, theme='streamlit')