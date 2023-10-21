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
info_screen = st.empty()
map_screen = st.empty()

m = folium.Map(location = (45.404028, -75.544722), zoom_start = 12)

info_screen.subheader("Loading map data...  Be patient this will take a while!")

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

# gdf.astype({'patch_number': 'int32'})

total_rows = gdf.shape[0]

select_gdf = gdf

filtered_df = dataframe_explorer(gdf, case=False)

filt_rows = filtered_df.shape[0]

st.write('Total number of rows (unfiltered)', total_rows )
st.write('Number of filtered rows = ', filt_rows)

def add_filt_patch_id(df):
    for i in range(len(df)):
        df.loc[i, 'filt_patch_id'] = i
    return df

filtered_df = add_filt_patch_id(filtered_df)

# filtered_df = filtered_df.astype({'filt_patch_id':'int'})


def mapIt(df):

    m = df.explore(column = 'Priority',
                   tiles =  'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
                   attr = 'Esri',
                   tooltip = True, 
                   popup = True, 
                   color = 'priorityColour', 
                   name='Planting Priority',
                   categorical=True,
                   legend=True,
                   style_kwds={'stroke':True, 'color':'black', 'weight': 1})
    

    #have an ESRI satellite image as an optional base map
    folium.TileLayer(
        tiles = 'OpenStreetMap',
        attr = 'Open Street Map',
        name = 'Satellite',
        overlay = False,
        control = True
        ).add_to(m)

    # add a fullscreen option and layer control to the map
    Fullscreen().add_to(m)
    folium.LayerControl().add_to(m)

    return m

def next_patch(n):
    
    m = mapIt(filtered_df.iloc[n:n+1,:])

    folium_static(m)

start_number = st.number_input("Start at", value = 0)

if 'patch_number' not in st.session_state:
    st.session_state['patch_number'] = 0
st.session_state['patch_number'] = start_number


if 'patch_number' not in st.session_state:
    st.session_state['patch_number'] = 0
if st.button('next patch'):
    st.session_state['patch_number'] += 1
if st.button('previous patch'):
    st.session_state['patch_number'] -= 1

# st.write(f'Filtered Patch Number: {st.session_state["patch_number"]}')

# st.write(filtered_df.iloc[st.session_state["patch_number"]:st.session_state["patch_number"]+1,:])

m = mapIt(filtered_df.iloc[st.session_state["patch_number"]:st.session_state["patch_number"]+1,:])

folium_static(m)

info_screen.empty()

