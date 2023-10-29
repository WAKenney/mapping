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

# from pandas.api.types import (
#     is_categorical_dtype,
#     is_datetime64_any_dtype,
#     is_numeric_dtype,
#     is_object_dtype)

st.header("ORYF")

m = folium.Map(location = (45.404028, -75.544722), zoom_start = 12)

st.subheader("Selecting Patches")

info_screen = st.empty()
main_screen = st.empty()

def get_geopackage():

    # Load geopackage and convert it to a GeoDataFrame

    try:

        uploaded_file = st.file_uploader("Choose a file", key = 1)
            
        if uploaded_file is not None:

            df = gpd.read_file(uploaded_file)
        
        return df
    
    except UnboundLocalError:
        st.warning('You must select a file to upload first.', icon="⚠️")

    



def get_some_csv_data():

    # Load csv and convert it to a GeoDataFrame

    uploaded_file = st.file_uploader("Choose a file", key = 1)
        
    if uploaded_file is not None:

        df = pd.read_csv(uploaded_file)

        gdf = gpd.GeoDataFrame(df, geometry=gpd.GeoSeries.from_wkt(df['geometry']))

        gdf = gdf.set_crs(4326)

    return gdf


#get the share link for the data file form one drive and past below
onedrive_link = 'https://1drv.ms/u/s!Alu-nJHZ-vTw83vNKAt2C0AwRpaD?e=u7cDaX' #High Medium Low


@st.cache_data(show_spinner=True)
def get_all_data():
    
    def load_onedrive (onedrive_link):
            
        # this converts the share link from above to a file name readable by pandas etc.
        data_bytes64 = base64.b64encode(bytes(onedrive_link, 'utf-8'))
        data_bytes64_String = data_bytes64.decode('utf-8').replace('/','_').replace('+','-').rstrip("=")
        resultUrl = f"https://api.onedrive.com/v1.0/shares/u!{data_bytes64_String}/root/content"
        return resultUrl

    fileName = load_onedrive(onedrive_link)

    gdf = gpd.read_file(fileName)

    gdf = gdf.to_crs(4326)

    for i in range(len(gdf)):
        gdf.loc[i, 'filt_patch_id'] = i

    return gdf


def test_if_df(df):
    if isinstance(df, gpd.GeoDataFrame):
        st.write('Yes, it is a GeoDataFrame!')
    else:
        st.write('No, it is not a GeoDataFrame.')


def mapIt(df):
    '''Creates a mapp showing the polygons in a given dataframe df'''

    m = df.explore(column = 'Priority',
                   tiles =  'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
                   attr = 'Esri',
                   tooltip = True, 
                   popup = True, 
                   color = 'priorityColour', 
                   name='Current Patch',
                   categorical=True,
                   legend=True,
                   style_kwds={'stroke':True, 'color':'yellow', 'weight': 3, 'fillOpacity':0})
    

    #have an ESRI satellite image as an optional base map
    folium.TileLayer(
        tiles = 'OpenStreetMap',
        attr = 'Open Street Map',
        name = 'Open Street Map',
        overlay = False,
        control = True
        ).add_to(m)

    # add a fullscreen option and layer control to the map
    Fullscreen().add_to(m)
    folium.LayerControl().add_to(m)

    return m

with info_screen.container():
    data_source_type = st.radio("Where do you want to get your data?", options = ["Geopackage", "All in Ottawa East", "From a file you select"])

    if data_source_type == "Geopackage":

        gdf = get_geopackage()

    elif data_source_type == 'All in Ottawa East':
        
        gdf = get_all_data()

    else:

        gdf = get_some_csv_data()


# test_if_df(gdf)

# gdf = gdf.set_crs(4326)

# if gdf is not None:
#     st.write("gdf crs = ", gdf.crs)

gdf = gdf.to_crs(4326)

total_rows = gdf.shape[0]

filtered_df = dataframe_explorer(gdf, case=False)

if filtered_df is not None:
    
    st.download_button("Press to download the filtered data file to your 'Downloads' directory.",
                        filtered_df.to_csv(index=False).encode('utf-8'),
                        "filtered_data.csv",
                        "text/csv",
                        key='download-csv'
                        )



# #put filtered_df into session_state
# if 'filtered_df' not in ss:
#     ss['filtered_df'] = []

# ss['filtered_df'] = filtered_df

#get the number of rows in filtered_df
filt_rows = filtered_df.shape[0]



# setup a panel with 3 columns
datacol1, datacol2, datacol3 = st.columns(3)

with datacol1:
    st.write('Total number of rows', total_rows )

with datacol2:
    st.write('Number of filtered rows ', filt_rows)

# enter a patch number to start at
with datacol3:
    start_number = st.number_input("Start at", value = 0)

# setup another panel with 5 buttons
button1, button2, button3, button4, button5 = st.columns(5)

if 'patch_number' not in ss:
    ss['patch_number'] = 0

with button1:    
    if st.button('next patch'):
        ss['patch_number'] += 1

with button2:
    if st.button('previous patch'):
        ss['patch_number'] -= 1

#set the current patch
current_patch = filtered_df.iloc[ss["patch_number"]:ss["patch_number"]+1,:]

#display the current patch data
st.subheader("Current Patch ")

st.write(current_patch)

#set up buttons to do various tasks
with button3:
    if st.button('SELECT Patch'):

        current_patch['centroid'] = current_patch['geometry'].centroid

        if 'selected_df' not in ss:

            ss.selected_df = current_patch

        ss.selected_df = pd.concat([ss.selected_df, current_patch])


with button4:

    if 'selected_df' in ss:
    
        ss['selected_df'] = ss['selected_df'].drop_duplicates(subset=['PIN']) 
        
        # convert to CSV
        csv = ss['selected_df'].to_csv(index=False)

        # create a download button
        st.download_button(
            label='Download Selected',
            data=csv,
            file_name='selected.csv',
            mime='text/csv'
        )


with button5:
    if st.button('This will re-set the selected patches.  Continue?'):
        if st.button('Are you sure you want to clear the list of selected patches?'):
            del ss.selected_df
            
    
m = mapIt(current_patch)

if st.button("View a map of the selected pach.", key="selected"):

    st.write('This is the selected_df')
    
    selected_df_map = mapIt(ss['selected_df'])
    
    folium_static(selected_df_map)


folium_static(m)

#display tthe accumulated selected patches this far
if 'selected_df' in ss:
    st.subheader("These are the selected patches so far")
    st.write(ss.selected_df.drop_duplicates(subset=['PIN']))
else:
    st.subheader("There are no selected patches yet.")



##################################################