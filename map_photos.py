from GPSPhoto import gpsphoto
import os
import streamlit as st


path = "C:/Users/pythonproject" # path to image folder

for i in os.listdir(path):
    data = gpsphoto.getGPSData(os.path.join(path,i))
    print(i, data['Latitude'], data['Longitude'])
