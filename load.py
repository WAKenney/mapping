import streamlit as st
import pandas as pd
import geopandas as gpd

st.title("Load a CSV File")

def get_file():
    uploaded_file = st.file_uploader("Choose a file")
        
    if uploaded_file is not None:

        df = pd.read_csv(uploaded_file)

        return df
    
csv_file = get_file()

if csv_file is not None:
    gdf = gpd.GeoDataFrame(csv_file, geometry=csv_file['geometry'])

st.write(csv_file)