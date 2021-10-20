import streamlit as st
from PIL import Image
from apps import home,image,video

import os
base_path=os.getcwd()
st.set_page_config(page_title='PhysioApp',page_icon='💡',menu_items={
'About': "An ML based Physio therapy improvement monitoring app by DNYIndia",
'Get help': "http://www.dnyindia.in",
'Report a bug': None
})

logincread=[["deepayan","BabaMaa"]]
menu=["Home","image","video"]

def main():
    st.sidebar.title("Enter User Details")
    username = st.sidebar.text_input("User name")
    password = st.sidebar.text_input("Password", type='password')
    st.sidebar.title("Select Tool")
    choice = st.sidebar.selectbox("Tools Menu", menu)
    if choice == "Home":
        home.app()
    for i in logincread:
        if i[0] == username and i[1] == password:
            st.sidebar.success("Login Successful as {}".format(username))
            if choice == "image":
                image.app()
            elif choice == "video":
                video.app()
        elif len(username)<1 or len(username)<1:
            if choice == "image":
                st.error("Login first in order to use this tool")
            elif choice == "video":
                st.error("Login first in order to use this tool")
        else:
            if choice == "image":
                st.error("Login first in order to use this tool")
            elif choice == "video":
                st.error("Login first in order to use this tool")
            st.sidebar.error("Username or Password mismatch!")



if __name__ == '__main__':
    main()