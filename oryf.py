import base64
import folium
from folium.plugins import Fullscreen
import geopandas as gpd
import pandas as pd
import streamlit as st
from streamlit_folium import folium_static
from streamlit_extras.dataframe_explorer import dataframe_explorer 


# from pandas.api.types import (
#     is_categorical_dtype,
#     is_datetime64_any_dtype,
#     is_numeric_dtype,
#     is_object_dtype)

st.header("ORYF")
screen1 = st.empty()

m = folium.Map(location = (45.404028, -75.544722), zoom_start = 12)

screen1.subheader("Loading map data...  Be patient this will take a while!")

#get the share link for the data file form one drive and past below
# onedrive_link = 'https://1drv.ms/u/s!Alu-nJHZ-vTw8wUirrIMsP5SxVPS?e=nyljiN' #High Medium
onedrive_link = 'https://1drv.ms/u/s!Alu-nJHZ-vTw83vNKAt2C0AwRpaD?e=u7cDaX' #High Medium Low

@st.cache_data(show_spinner=True)
def getData():
    
    def load_onedrive (onedrive_link):
            
        # this converts the share link from above to a file name readable by pandas etc.
        data_bytes64 = base64.b64encode(bytes(onedrive_link, 'utf-8'))
        data_bytes64_String = data_bytes64.decode('utf-8').replace('/','_').replace('+','-').rstrip("=")
        resultUrl = f"https://api.onedrive.com/v1.0/shares/u!{data_bytes64_String}/root/content"
        return resultUrl

    fileName = load_onedrive(onedrive_link)

    gdf = gpd.read_file(fileName)

    gdf = gdf.to_crs(4326)

    return gdf

gdf = getData()

select_gdf = gdf

filtered_df = dataframe_explorer(gdf, case=False)

st.write(filtered_df.head(2))

def mapIt(df):

    m = df.explore(column = 'Priority', 
                        tooltip = True, 
                        popup = True, 
                        color = 'priorityColour', 
                        name='Planting Priority',
                        categorical=True,
                        legend=True,
                        style_kwds={'stroke':True, 'color':'black', 'weight': 1})
    

    #have an ESRI satellite image as an optional base map
    folium.TileLayer(
        tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr = 'Esri',
        name = 'Satellite',
        overlay = False,
        control = True
        ).add_to(m)

    # add a fullscreen option and layer control to the map
    Fullscreen().add_to(m)
    folium.LayerControl().add_to(m)

    return m

start_number = st.number_input("Start at", value = 0)

r=start_number

m = mapIt(select_gdf.iloc[r:r+1,:])


folium_static(m)

screen1.empty()

