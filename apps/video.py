import streamlit as st
import cv2
import numpy as np
import pose_module as pm
from PIL import Image
import tempfile

detector=pm.poseDetector(mode=False)
def addtext(image,text):
    h,w,_=image.shape
    font = cv2.FONT_HERSHEY_SIMPLEX
    org = (20, w-int(w*.5))
    print(org)
    fontScale = int(w*.001)
    if fontScale<1:
        fontScale=1
    color = (255, 0, 0)
    thickness = 4
    image = cv2.putText(image,str(text), org, font, fontScale, color, thickness, cv2.LINE_AA)
    return image
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
    e_ang = st.number_input("Max movement Angel", max_value=180)
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

            try:
                while vid.isOpened():
                    ret, frame = vid.read()
                    detection_image, angle = detection(frame, nums_pos[detection_on])
                    if angle>e_ang:
                        continue
                    if max_ang==0 and min_ang==0:
                        max_ang=angle
                        min_ang=angle
                    if max_ang<angle:
                        max_ang=angle
                    if min_ang>angle:
                        min_ang=angle
                    img=addtext(detection_image,"Max angel : {} and Min angel : {} ".format(max_ang, min_ang))
                    k = 4
                    width = int((frame.shape[1]) / k)
                    height = int((frame.shape[0]) / k)
                    scaled = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)
                    stframe.image(scaled, channels='BGR', use_column_width=True)

            except:
                st.write("Done Processing")
            st.write("Max angel : {}° and Min angel : {}° ".format(max_ang, min_ang))
            vid.release()


