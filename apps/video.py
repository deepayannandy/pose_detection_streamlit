import streamlit as st
import cv2
import numpy as np
import pose_module as pm
from PIL import Image
import tempfile

detector=pm.poseDetector(mode=False)
def detection(img,num):
    img_get = detector.find_pos(img, False)
    lm_list = detector.find_landmark(img, False)
    ang = 0
    try:
        if len(lm_list) != 0:
            if num == 1:
                ang = detector.find_angel(img, 16, 14, 12)
            elif num == 2:
                ang = detector.find_angel(img, 15, 13, 11)
            elif num == 3:
                ang = detector.find_angel(img, 28, 26, 24)
            elif num == 4:
                ang = detector.find_angel(img, 27, 25, 23)
            elif num == 5:
                ang = detector.find_angel(img, 14, 12, 24)
            elif num == 6:
                ang = detector.find_angel(img, 13, 11, 23)
            elif num == 7:
                ang = detector.find_angel(img, 26, 24, 12)
            elif num == 8:
                ang = detector.find_angel(img, 25, 23, 11)
    except:
        pass
    return img_get, int(ang)
detections=['Left elbow','Right elbow','Left knee','Right knee','Left solder','Right solder','Left hip','Right hip']
nums_pos={'Left elbow':1,'Right elbow':2,'Left knee':3,'right knee':4,'Left solder':5,'Right solder':6,'Left hip':7,'Right hip':8}

def app():
    st.header("Physio App: Improvement using Video")
    detection_on = st.selectbox("Body part", detections)
    file_video = st.file_uploader("Upload Image", type=['mp4', 'mov'])
    temp=tempfile.NamedTemporaryFile(delete=False)
    button = st.button("Process")
    stframe=st.empty()
    max_ang=0
    min_ang=0
    if button:
        if not file_video:
            st.text("No video Selected")
        else:
            temp.write(file_video.read())
            vid=cv2.VideoCapture(temp.name)

            while vid.isOpened():
                ret, frame = vid.read()
                detection_image, angle = detection(frame, nums_pos[detection_on])
                k = 4
                width = int((frame.shape[1]) / k)
                height = int((frame.shape[0]) / k)
                scaled = cv2.resize(detection_image, (width, height), interpolation=cv2.INTER_AREA)
                stframe.image(scaled, channels='BGR', use_column_width=True)
            vid.release()


