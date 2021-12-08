import streamlit as st
from PIL import Image
from apps import home,image,video,face

import os
base_path=os.getcwd()
st.set_page_config(page_title='PhysioApp',page_icon='💡',menu_items={
'About': "An ML based Physio therapy improvement monitoring app by Omphalos Birj Cooperation",
'Get help': "http://www.dnyindia.in",
'Report a bug': None
})
def getUserData():
    allUserData=[]
    f = open(base_path+"/staticdata/userdata.txt", 'r')
    lines = f.readlines()
    for line in lines:
        data=str(line).replace('\n','').split('?')
        allUserData.append(data)
    return allUserData

logincread=getUserData()
menu=["Home","Image","Video","Facial"]


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
            if choice == "Image":
                image.app(i)
            elif choice == "Video":
                video.app()
            elif choice == "Facial":
                face.app(i)
        elif len(username)<1 or len(username)<1:
            if choice == "image":
                st.error("Login first in order to use this tool")
            elif choice == "video":
                st.error("Login first in order to use this tool")
            elif choice == "Facial":
                st.error("Login first in order to use this tool")




if __name__ == '__main__':
    main()