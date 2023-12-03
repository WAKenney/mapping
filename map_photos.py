from GPSPhoto import gpsphoto
import os
import streamlit as st

path = st.sidebar.file_uploader("Upload a file", type="dir")
if path is not None:
    st.write("You selected the following folder:", path)

for i in os.listdir(path):
    if i.endswith(".jpg"):
        data = gpsphoto.getGPSData(os.path.join(path,i))
        st.write(i, data['Latitude'], data['Longitude'])