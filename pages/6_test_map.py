import geopandas as gpd
from shapely.geometry import Point
import folium
from folium.plugins import Fullscreen
import streamlit as st
from streamlit_folium import folium_static
from streamlit_extras.dataframe_explorer import dataframe_explorer 
import base64

ss = st.session_state

st.title('Test Map')

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

    gdf = gdf.to_crs(4326)

    for i in range(len(gdf)):
        gdf.loc[i, 'filt_patch_id'] = i

    return gdf

# gdf = getData()

# gdf.set_crs(epsg=4326).to_crs(epsg=32618)

# m= gdf.explore()

# Create a Shapely Point object
point = Point(-75.50129628926985, 45.46048707770084)
buffer = point.buffer(100)

# Create a GeoSeries containing the polygon geometry
buffer_series = gpd.GeoSeries(buffer)
buffer_series.set_crs(epsg=4326).to_crs(epsg=32618)

# Create a GeoDataFrame containing the GeoSeries
buffer_gdf = gpd.GeoDataFrame(geometry=buffer_series)

# Visualize the GeoDataFrame using gpd.explore()
m = buffer_gdf.explore()

Fullscreen().add_to(m)
folium.LayerControl().add_to(m)


folium_static(m)

