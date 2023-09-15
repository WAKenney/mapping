import base64
import geopandas as gpd
import streamlit as st
import folium
from folium.plugins import Fullscreen
from streamlit_folium import folium_static

st.write("Test")

#get the share link for the data file form one drive and past below
onedrive_link = 'https://1drv.ms/u/s!Alu-nJHZ-vTw1gZM_jZm6VqK98Ga?e=EK9Z6b'


@st.cache_data(show_spinner=False)
def load_onedrive (onedrive_link):
           
    # this converts the share link from above to a file name readable by pandas etc.
    data_bytes64 = base64.b64encode(bytes(onedrive_link, 'utf-8'))
    data_bytes64_String = data_bytes64.decode('utf-8').replace('/','_').replace('+','-').rstrip("=")
    resultUrl = f"https://api.onedrive.com/v1.0/shares/u!{data_bytes64_String}/root/content"
    return resultUrl

fileName = load_onedrive(onedrive_link)




gdf = gpd.read_file(fileName)

m = folium.Map(location = (45.404028, -75.544722), zoom_start = 12)

st.write(gdf)


folium_static(m)