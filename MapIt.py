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

# def get_geopackage():

#     # Load geopackage and convert it to a GeoDataFrame

#     try:

#         uploaded_file = st.file_uploader("Choose a file", key = 1)
            
#         if uploaded_file is not None:

#             df = gpd.read_file(uploaded_file)
        
#         return df
    
#     except UnboundLocalError:
#         st.warning('You must select a file to upload first.', icon="⚠️")

# gdf = get_geopackage()

ncc_all = gpd.read_file('ncc_all.gpkg')

# all_ncc_gpd = gpd.read_file('ALL NCC Parcels in SNCA.gpkg')

# snca_gpd = gpd.read_file('ncc_all.gpkg')

ncc_all.drop(columns=['Hectares', 'TotalWtcount', 'TotalWtmean', 'TotalWtmedian', 'TotalWtmajority', 
                  'CLI1-mean', 'CLI1-median', 'CLI1-majority'], inplace=True)

# ncc_all = dataframe_explorer(gdf, case=False)

exploded_ncc_all = ncc_all.explode()

exploded_ncc_all['Hectares'] = ((exploded_ncc_all['geometry'].area)/10000).round(1)

exploded_ncc_all = exploded_ncc_all.query('Hectares >25')

st.write(exploded_ncc_all)

def mapIt(gdf):
    '''Creates a mapp showing the polygons in a given dataframe df'''

    m = gdf.explore(name = 'ALL NCC',
                   style_kwds={'stroke':True, 'color':'purple', 'weight': 3, 'fillOpacity':0})
    
    # all_ncc_gpd.explore(m = m, name = 'ALL NCC in SNCA Watershed', show = False,
    #                style_kwds={'stroke':True, 'color':'yellow', 'weight': 2, 'fillOpacity':0})
    
    # snca_gpd.explore(m = m, name = 'SNCA Watershed', show = False,
    #                style_kwds={'stroke':True, 'color':'green', 'weight': 2, 'fillOpacity':0})
   
    # folium.TileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    #                  name='Satelite', attr = 'ESRI').add_to(m)

    # add a fullscreen option and layer control to the map
    Fullscreen().add_to(m)
    folium.LayerControl().add_to(m)

    return m
       
m = mapIt(exploded_ncc_all)

folium_static(m)

info_screen.empty()