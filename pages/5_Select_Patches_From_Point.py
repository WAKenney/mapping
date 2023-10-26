import streamlit as st
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from streamlit_folium import folium_static
import folium
from folium.plugins import Fullscreen
import base64


ss = st.session_state

st.title("Select Polygons by Distance From Point")


st.subheader("Loading map data...  Be patient this will take a while!")


# m = folium.Map(location = (45.46138994807266, -75.50006308751581), zoom_start = 12)

#get the share link for the data file form one drive and past below
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

    return gdf


#Read a geopackage

def get_buffer():
    
    file_name = st.file_uploader("Choose buffer file")

    if file_name is not None:

        gdf = gpd.read_file(file_name)
        
        return gdf


polygon_gdf = getData()

polygon_gdf = polygon_gdf.to_crs(3857)

st.write(polygon_gdf.crs)

buffer_gdf = get_buffer()

st.write(buffer_gdf.crs)

orleans_polygons = polygon_gdf[polygon_gdf.within(buffer_gdf.geometry.iloc[0])]

st.write(orleans_polygons.shape)
st.write(orleans_polygons.crs)


st.write(orleans_polygons.crs)

orleans_polygons = orleans_polygons.to_crs(4326)

st.write(orleans_polygons.crs)

m = orleans_polygons.explore()


folium_static(m)