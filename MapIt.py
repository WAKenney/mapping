import base64
import folium
from folium.plugins import Fullscreen
import geopandas as gpd
import pandas as pd
import streamlit as st
from streamlit_folium import folium_static
from streamlit_extras.dataframe_explorer import dataframe_explorer
import os
import platform
from datetime import datetime

ss = st.session_state

st.header("MapIt")
info_screen = st.empty()
map_screen = st.empty()

m = folium.Map(location = (45.404028, -75.544722), zoom_start = 12)

ncc_all = gpd.read_file('ncc_all.gpkg')

ncc_all.drop(columns=['Hectares', 'TotalWtcount', 'TotalWtmean', 'TotalWtmedian', 'TotalWtmajority', 
                  'CLI1-mean', 'CLI1-median', 'CLI1-majority'], inplace=True)

exploded_ncc_all = ncc_all.explode()

exploded_ncc_all['Hectares'] = ((exploded_ncc_all['geometry'].area)/10000).round(1)

exploded_ncc_all = exploded_ncc_all.query('Hectares >25')

st.write(exploded_ncc_all)

ncc_in_snca_gdf = gpd.read_file('ncc_in_snca.gpkg')

ncc_in_snca_gdf.drop(columns=['Hectares', 'TotalWtcount', 'TotalWtmean', 'TotalWtmedian', 'TotalWtmajority', 
                  'CLI1-mean', 'CLI1-median', 'CLI1-majority'], inplace=True)

ncc_in_snca_gdf = ncc_in_snca_gdf.explode()

ncc_in_snca_gdf['Hectares'] = ((ncc_in_snca_gdf['geometry'].area)/10000).round(1)

ncc_in_snca_gdf = ncc_in_snca_gdf.query('Hectares >= 25')

study_area_gdf = gpd.read_file('study_area.gpkg')

snca_boundary_gdf = gpd.read_file('snca_boundary.gpkg')


def mapIt():
    '''Creates a mapp showing the polygons in a given dataframe df'''

    m = exploded_ncc_all.explore(name = 'ALL NCC Parcels',
                   style_kwds={'stroke':True, 'color':'purple', 'weight': 3, 'fillOpacity':0})
    
    study_area_gdf.explore(m=m, name = "Ottawa Wards 1, 2, 19 and 20", show = False,
                           style_kwds={'stroke':True, 'color':'yellow', 'weight': 2, 'fill': False, 'fillOpacity':0})
    
    ncc_in_snca_gdf.explore(m=m, name = "NCC Parcels in SNCA Watershed", show = False,
                           style_kwds={'stroke':True, 'color':'blue', 'weight': 2, 'fillOpacity':0})
    
    snca_boundary_gdf.explore(m = m, name = 'SNCA Watershed', show = False,
                   style_kwds={'stroke':True, 'color':'green', 'weight': 2,  'fill': False, 'fillOpacity':0})
   
    folium.TileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
                     name='Satelite', attr = 'ESRI').add_to(m)

    # add a fullscreen option and layer control to the map
    Fullscreen().add_to(m)
    folium.LayerControl().add_to(m)

    return m
       
m = mapIt()

folium_static(m)

save_map_button = st.button("Do you want to save the map as an HTML file?")

if save_map_button:
    # Get the current date and time
    current_date_time = datetime.now()

    save_file_name = 'ncc_patches_' + str(current_date_time) + '.html'

    m.save(save_file_name)

info_screen.empty()