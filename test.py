import geopandas as gpd
import streamlit as st
import folium
from folium.plugins import Fullscreen
from streamlit_folium import folium_static

st.write("Test")

fileName = r"HallRoad.gpkg"
gdf = gpd.read_file(fileName)

m = folium.Map(location = (45.404028, -75.544722), zoom_start = 12)




folium_static(m)