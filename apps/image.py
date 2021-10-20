import streamlit as st
import cv2
import numpy as np
import pose_module as pm
from PIL import Image

detector=pm.poseDetector()
def detection(img,num):
    img_get = detector.find_pos(img, False)
    lm_list = detector.find_landmark(img, False)
    ang=0
    try:
        if len(lm_list) != 0:
            if num==1:
                ang = detector.find_angel(img, 12, 14, 16)
            elif num==2:
                ang = detector.find_angel(img, 11, 13, 15)
            elif num==3:
                ang = detector.find_angel(img, 24, 26, 28)
            elif num==4:
                ang = detector.find_angel(img, 23, 25, 27)
    except:
        pass
    return img_get,int(ang)
detections=['Left elbow','Right elbow','Left knee','right knee']
nums_pos={'Left elbow':1,'Right elbow':2,'Left knee':3,'right knee':4}
def app():
    st.header("Physio App: Improvement using Image")
    detection_on=st.selectbox("Body part",detections)
    file_image=st.file_uploader("Upload Image",type=['jpeg','jpg','png'])
    button= st.button("Process")
    if button:
        detection_image, angle = detection(np.array(Image.open(file_image)),nums_pos[detection_on])
        st.image(detection_image)
        st.write("## Generated Angel is : {} °".format(angle))
    else:
        st.write("Upload an image")
