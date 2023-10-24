import streamlit as st
import pandas as pd
import geopandas as gpd
from streamlit_folium import folium_static

ss = st.session_state

st.title("Load a CSV File")

st.title("GeoDataFrame to CSV and back to GeoDataFrame")
st.write("This app converts a GeoDataFrame to a CSV file, saves it, and then loads the CSV file back to a GeoDataFrame.")

def csv_to_gdf():

    # Load csv and convert it to a GeoDataFrame

    uploaded_file = st.file_uploader("Choose a file", key = 1)
        
    if uploaded_file is not None:

        df = pd.read_csv(uploaded_file)

    return gpd.GeoDataFrame(df, geometry=gpd.GeoSeries.from_wkt(df['geometry']))


gdf = csv_to_gdf()

# Verify that it's a GeoDataFrame
if isinstance(gdf, gpd.GeoDataFrame):
    st.header("It's a GeoDataFrame")
    
gdf_name = st.text_input("What do you want to call your geodataframe?")

if gdf_name is not None:

    if gdf_name not in ss:
        ss[gdf_name] = ' '

    ss[gdf_name] = gdf_name


