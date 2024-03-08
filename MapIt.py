import base64
import folium
from folium.plugins import Fullscreen
import geopandas as gpd
import pandas as pd
import streamlit as st
from streamlit_folium import folium_static
from streamlit_extras.dataframe_explorer import dataframe_explorer
import os

ss = st.session_state

st.header("MapIt")
info_screen = st.empty()
map_screen = st.empty()

m = folium.Map(location = (45.404028, -75.544722), zoom_start = 12)

# st.title("Load a geopackage file")


def get_geopackage():

    # Load geopackage and convert it to a GeoDataFrame

    try:

        uploaded_file = st.file_uploader("Choose a file", key = 1)
            
        if uploaded_file is not None:

            df = gpd.read_file(uploaded_file)
        
        return df
    
    except UnboundLocalError:
        st.warning('You must select a file to upload first.', icon="⚠️")

gdf = get_geopackage()

gdf.drop(columns=['Hectares', 'TotalWtcount', 'TotalWtmean', 'TotalWtmedian', 'TotalWtmajority', 
                  'CLI1-mean', 'CLI1-median', 'CLI1-majority'], inplace=True)

gdf = dataframe_explorer(gdf, case=False)


exploded_gdf = gdf.explode()

exploded_gdf['Hectares'] = ((exploded_gdf['geometry'].area)/10000).round(1)

exploded_gdf = exploded_gdf.query('Hectares >25')


def mapIt(gdf):
    '''Creates a mapp showing the polygons in a given dataframe df'''

    m = gdf.explore(tiles =  'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
                   attr = 'Esri',
                   style_kwds={'stroke':True, 'color':'yellow', 'weight': 2, 'fillOpacity':0})
    

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
       
m = mapIt(exploded_gdf)

folium_static(m)

info_screen.empty()






