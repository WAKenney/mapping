import streamlit as st
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from streamlit_folium import folium_static
import folium
from folium.plugins import Fullscreen
import base64


ss = st.session_state

st.title("Select Polygons by Distance From Point")


st.subheader("Loading map data...  Be patient this will take a while!")


# m = folium.Map(location = (45.46138994807266, -75.50006308751581), zoom_start = 12)

#get the share link for the data file form one drive and past below
onedrive_link = 'https://1drv.ms/u/s!Alu-nJHZ-vTw83vNKAt2C0AwRpaD?e=u7cDaX' #High Medium Low

@st.cache_data(show_spinner=True)
def get_data():
    
    def load_onedrive (onedrive_link):
            
        # this converts the share link from above to a file name readable by pandas etc.
        data_bytes64 = base64.b64encode(bytes(onedrive_link, 'utf-8'))
        data_bytes64_String = data_bytes64.decode('utf-8').replace('/','_').replace('+','-').rstrip("=")
        resultUrl = f"https://api.onedrive.com/v1.0/shares/u!{data_bytes64_String}/root/content"
        return resultUrl

    fileName = load_onedrive(onedrive_link)

    gdf = gpd.read_file(fileName)

    return gdf

polygon_gdf = get_data()

def test_if_df(df):
    if isinstance(df, gpd.GeoDataFrame):
        st.write('Yes, it is a GeoDataFrame!')
    else:
        st.write('No, it is not a GeoDataFrame.')

polygon_gdf.to_crs(3857, inplace = True)

test_if_df(polygon_gdf)

st.write(polygon_gdf.crs)


def get_buffer():
    
    file_name = st.file_uploader("Choose buffer file")

    if file_name is not None:

        gdf = gpd.read_file(file_name)
        
        return gdf


def create_buffer():
    point = Point(45.46093652229643, -75.48770910276248)

    return gpd.GeoDataFrame(geometry=[point.buffer(12000)], crs = 3857)

buffer_gdf = create_buffer()

buffer_gdf.to_crs(3857, inplace = True)

test_if_df(buffer_gdf)

st.write(polygon_gdf.crs)

# buffer_gdf = get_buffer()

# orleans_polygons = polygon_gdf[polygon_gdf.within(buffer_gdf.geometry.iloc[0])]

orleans_polygons = gpd.overlay(polygon_gdf, buffer_gdf, how='intersection')

st.write(orleans_polygons)

# test_if_df(orleans_polygons)

# st.write(orleans_polygons)



orleans_polygons = orleans_polygons.to_crs(4326)

m = orleans_polygons.explore()

polygon_gdf.to_crs(crs = 4326, inplace = True)

st.write("AHHH",polygon_gdf.crs)

m = polygon_gdf.explore()

buffer_gdf.to_crs(crs = 4326, inplace = True)

st.write(buffer_gdf)

buffer_gdf.explore().add_to(m)

def save_file(df):
    df_csv = df.to_csv(index=False).encode('utf-8')

    st.download_button("Press to Download File.",
                        df_csv,
                        "File.csv",
                        "text/csv",
                        key='download-csv'
                        )

if st.button("Save the file?"):
    save_file(orleans_polygons)

folium_static(m)