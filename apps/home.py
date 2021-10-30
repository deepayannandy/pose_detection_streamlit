import streamlit as st
from PIL import Image
import os
base_path=os.getcwd()

def app():
    st.image(Image.open(base_path+"/comp_logo/logo0.jpeg"))
    st.title("Physio App")
    st.write('This is a webapp specially designed for creating improvement reports for physiotherapy patients using ML')

    st.write('In order to use this app you have to login with your valid credentials.')
