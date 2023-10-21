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


total_rows = gdf.shape[0]

select_gdf = gdf

filtered_df = dataframe_explorer(gdf, case=False)

filt_rows = filtered_df.shape[0]

datacol1, datacol2, datacol3 = st.columns(3)

with datacol1:
    st.write('Total number of rows (unfiltered)', total_rows )

with datacol2:
    st.write('Number of filtered rows = ', filt_rows)

def add_filt_patch_id(df):
    for i in range(len(df)):
        df.loc[i, 'filt_patch_id'] = i
    return df

filtered_df = add_filt_patch_id(filtered_df)

save_filtered_data = st.button('Click here to save the filtered data')
if save_filtered_data:
    filtered_df.to_file('dataframe.gpkg', driver='GPKG', layer='name') 

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
                   style_kwds={'stroke':True, 'color':'yellow', 'weight': 1, 'fillOpacity':0})
    

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

with datacol3:
    start_number = st.number_input("Start at", value = 0)

button1, button2, button3 = st.columns(3)

if 'patch_number' not in st.session_state:
    st.session_state['patch_number'] = 0

with button1:    
    if st.button('next patch'):
        st.session_state['patch_number'] += 1

with button2:
    if st.button('previous patch'):
        st.session_state['patch_number'] -= 1

current_patch = filtered_df.iloc[st.session_state["patch_number"]:st.session_state["patch_number"]+1,:]

st.write(current_patch)

with button3:
    if st.button('Save Patch'):
        st.write('Hold')

m = mapIt(current_patch)

folium_static(m)


info_screen.empty()

