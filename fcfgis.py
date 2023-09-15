
import geopandas as gpd
import folium
import streamlit as st
from folium.plugins import Fullscreen
from streamlit_folium import folium_static


titlecol1, titlecol2, titlecol3 =st.columns([10,80,10])
with titlecol2:
   st.subheader("Priority Planting")

# fileName = r"E:\FCFGIS\FCFStreamlit\priority.gpkg"
fileName = r"priority.gpkg"

@st.cache_data(show_spinner=False)
def get_data():

    '''
    Get the GIS data as a geodataFrame
    '''
  
    if fileName is not None:
        
        gdf = gpd.read_file(fileName)
        gdf = gdf.to_crs(3857)

        gdf = gdf.round(decimals = 1)

        return gdf

with st.spinner('Please wait while the data are loaded.'):
   gdf = get_data()

   df = gpd.read_file(fileName, ignore_geometry = True)

# st.dataframe(df)

df['priorityColour'] = df['Priority'].map({'High':'red', 'Medium':'green', 'Low':'grey'})


def mapit():

   # Draw the map
   fcfMap = gdf.explore(column = 'Priority', 
                        tooltip = False, 
                        popup = True, 
                        color = 'priorityColour', 
                        name='Planting Priority',
                        categorical=True,
                        legend=True,
                        style_kwds={'stroke':True, 'color':'black', 'weight': 1})

   # Add photo layer
   folium.TileLayer(
         tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
         attr = 'Esri',
         name = 'Satellite',
         overlay = False,
         control = True
         ).add_to(fcfMap)

   # add a fullscreen option and layer control to the map
   Fullscreen().add_to(fcfMap)
   folium.LayerControl().add_to(fcfMap)

   # folium.plugins.MeasureControl().add_to(fcfMap)

   folium_static(fcfMap)


with st.spinner("Setting up the map ... be patient!"):
   mapit()