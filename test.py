import geodatasets
import geopandas as gpd
import streamlit as st
import folium
from folium.plugins import Fullscreen
from streamlit_folium import folium_static

st.write("Test")

# df = gpd.read_file(r"FCFPlantingPriority021221.gpkg")

# st.write(df.head(2)) 

# fcfMap = df.explore("LU_2015", cmap="Blues")

m = folium.Map(location = (45.404028, -75.544722), zoom_start = 12)


folium_static(m)