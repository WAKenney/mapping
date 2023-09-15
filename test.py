import base64
import folium
from folium.plugins import Fullscreen
import geopandas as gpd
import pandas as pd
import streamlit as st
from streamlit_folium import folium_static


st.write("Test")

#get the share link for the data file form one drive and past below
onedrive_link = 'https://1drv.ms/u/s!Alu-nJHZ-vTw8wUirrIMsP5SxVPS?e=nyljiN'


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

gdf = getData()
select_gdf = gdf

with st.form('Filter Data'):

    param = st.selectbox("Select a parameter for your query.", gdf.columns)
    submitted = st.form_submit_button("Submit")
    
    if submitted:
        st.write("Your data will be filtered by " + param)

with st.form('Filter Data2'):

    val = st.selectbox('Select a value.', gdf[param].unique())
    
    submitted = st.form_submit_button("Submit")
    
    if submitted:
        st.write("You are filtering " + param + " by " + val)
        select_gdf = gdf.loc[gdf[param] == val]


def mapIt(df):
# Create and show the map
    df.to_json()
    m = folium.Map(location = (45.404028, -75.544722), zoom_start = 12)

    folium.GeoJson(df, name = 'Priorities').add_to(m)

    folium_static(m)

mapIt(select_gdf)