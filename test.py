import base64
import geopandas as gpd
import streamlit as st
import folium
from folium.plugins import Fullscreen
from streamlit_folium import folium_static

from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid.shared import JsCode
from st_aggrid.shared import GridUpdateMode

st.write("Test")

#get the share link for the data file form one drive and past below
onedrive_link = 'https://1drv.ms/u/s!Alu-nJHZ-vTw8wUirrIMsP5SxVPS?e=nyljiN'


@st.cache_data(show_spinner=False)
def load_onedrive (onedrive_link):
           
    # this converts the share link from above to a file name readable by pandas etc.
    data_bytes64 = base64.b64encode(bytes(onedrive_link, 'utf-8'))
    data_bytes64_String = data_bytes64.decode('utf-8').replace('/','_').replace('+','-').rstrip("=")
    resultUrl = f"https://api.onedrive.com/v1.0/shares/u!{data_bytes64_String}/root/content"
    return resultUrl

fileName = load_onedrive(onedrive_link)

gdf = gpd.read_file(fileName)

AgGrid(gdf)


# def aggFilter(agData):
    
#     """ This function sets up the grid to view and filter the data"""
    
#     df = agData.copy()

#     gb = GridOptionsBuilder.from_dataframe(df)
#     gb.configure_pagination(enabled=True)
#     gb.configure_default_column(editable=True, filter=True)


#     gridOptions = gb.build()

#     gridReturn = AgGrid(df,
#         gridOptions=gridOptions,
#         allow_unsafe_jscode=True,
#         height = 500, 
#         theme = 'streamlit',
#         enable_enterprise_modules=True, # enables right click and fancy features - can add license key as another parameter (license_key='string') if you have one
#         key='select_grid', # stops grid from re-initialising every time the script is run
#         reload_data=True, # allows modifications to loaded_data to update this same grid entity
#         update_mode=GridUpdateMode.MANUAL,
#         data_return_mode="FILTERED_AND_SORTED")

#     gridReturnData = gridReturn['data']



m = folium.Map(location = (45.404028, -75.544722), zoom_start = 12)

folium.GeoJson(gdf, name = 'Priorities').add_to(m)


st.write(gdf)


folium_static(m)