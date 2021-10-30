import streamlit as st
import cv2
import numpy as np
import pose_module as pm
from PIL import Image
import os, numpy
import generate_report as gr
base_path=os.getcwd()

detector=pm.poseDetector()
logo=cv2.imread(base_path+"/comp_logo/logo0.jpeg")
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
def colage(img1, img2):
    h1, w1 = img1.shape[:2]
    h2, w2 = img2.shape[:2]

    # create empty matrix
    vis = np.zeros((max(h1, h2), w1 + w2, 3), np.uint8)

    # combine 2 images
    vis[:h1, :w1, :3] = img1
    vis[:h2, w1:w1 + w2, :3] = img2
    return vis
def transparentOverlay(src, overlay, pos=(0, 0), scale=.2):
    """
    :param src: Input Color Background Image
    :param overlay: transparent Image (BGRA)
    :param pos:  position where the image to be blit.
    :param scale : scale factor of transparent image.
    :return: Resultant Image
    """
    overlay = cv2.resize(overlay, (0, 0), fx=scale, fy=scale)
    h, w, _ = overlay.shape  # Size of foreground
    rows, cols, _ = src.shape  # Size of background Image
    y, x = pos[0], pos[1]  # Position of foreground/overlay image
    # loop over all pixels and apply the blending equation
    for i in range(h):
        for j in range(w):
            if x + i >= rows or y + j >= cols:
                continue
            alpha = float(overlay[i][j][2] / 255.0)  # read the alpha channel
            src[x + i][y + j] = alpha * overlay[i][j][:3] + (1 - alpha) * src[x + i][y + j]
    return src
def addtext(image,text):
    h,w,_=image.shape
    font = cv2.FONT_HERSHEY_SIMPLEX
    org = (0, w-20)
    fontScale = 1
    color = (255, 0, 0)
    thickness = 2
    image = cv2.putText(image, 'Date:'+str(text), org, font, fontScale, color, thickness, cv2.LINE_AA)
    return image
detections=['Left elbow','Right elbow','Left knee','right knee']
nums_pos={'Left elbow':1,'Right elbow':2,'Left knee':3,'right knee':4}
def app():
    st.header("Physio App: Improvement using Image")
    detection_on=st.selectbox("Body part",detections)
    e_ang=st.number_input("Expected Angel",min_value=1)
    file_image1 = st.file_uploader("Upload Image1",type=['jpeg','jpg','png'])
    date1 = st.date_input('Image1 date')
    file_image2 = st.file_uploader("Upload Image2", type=['jpeg', 'jpg', 'png'])
    date2 = st.date_input('Image2 date')
    button= st.button("Process")
    if button:
        try:
            detection_image1, angle1 = detection(np.array(Image.open(file_image1)), nums_pos[detection_on])
            detection_image2, angle2 = detection(np.array(Image.open(file_image2)), nums_pos[detection_on])
            if angle1==0:
                st.write("We can not find any detection on Image1")
            if angle2==0:
                st.write("We can not find any detection on Image2")
            else:
                final_img=transparentOverlay(colage(addtext(detection_image1,date1),addtext(detection_image2,date2)),logo)
                st.image(final_img)
                st.write(" Generated Angel in image1 is is : {} ° or {} % of the expected angel".format(angle1,int((angle1/e_ang)*100)))
                st.write(" Generated Angel in image1 is is : {} ° or {} % of the expected angel".format(angle2,int((angle2/e_ang)*100)))
                st.write("### Overall improvement is: {} %".format((int((angle2/e_ang)*100)-int((angle1/e_ang)*100))))
        except:
            st.write("Something Went Wrong!")

    else:
        st.write("Upload an image")
