import streamlit as st
import cv2
import numpy as np
import pose_module as pm
from PIL import Image
import os, numpy
import generate_report as gr
import datetime
import pytz
tz_In = pytz.timezone('Asia/Kolkata')
time = datetime.datetime.now(tz_In)
base_path=os.getcwd()

detector=pm.poseDetector()
logo=cv2.imread(base_path+"/comp_logo/logo0.jpeg")
def detection(img):
    img_get = detector.find_pos(img, False)
    lm_list = detector.find_landmark(img, False)
    ang=0
    try:
        ang = detector.find_angel(img, 16, 14, 12)
    except:
        print("Something went wrong")
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
    org = (0, w-int(w*.1))
    fontScale = int(w*.001)
    if fontScale<1:
        fontScale=1
    color = (255, 0, 0)
    thickness = 4
    image = cv2.putText(image, 'Date:'+str(text), org, font, fontScale, color, thickness, cv2.LINE_AA)
    return image

sex=["Male","Female","Others"]
def app(userdata):
    userdata=userdata
    st.header("Physio App: Improvement using facial image")
    pname = st.text_input("Patients name")
    choiceS = st.selectbox("Sex", sex)
    page=st.number_input("Expected Age",min_value=5)
    pcontact = st.text_input("Patients Contact")
    file_image1 = st.file_uploader("Upload Image1",type=['jpeg','jpg','png'])
    date1 = st.date_input('Image1 date')
    file_image2 = st.file_uploader("Upload Image2", type=['jpeg', 'jpg', 'png'])
    date2 = st.date_input('Image2 date')
    button= st.button("Process")
    if button:
        try:
            detection_image1, angle1 = detection(np.array(Image.open(file_image1)))
            detection_image2, angle2 = detection(np.array(Image.open(file_image2)))
            if angle1==0:
                st.write("We can not find any detection on Image1")
            if angle2==0:
                st.write("We can not find any detection on Image2")
            else:
                final_img=colage(addtext(detection_image1,date1),addtext(detection_image2,date2))
                st.image(final_img)
                imagepath=base_path +"/collection/" +time.strftime("%I:%M-%d-%m-%y")+".png"
                cv2.imwrite(imagepath, cv2.cvtColor(final_img, cv2.COLOR_RGB2BGR))
                a=" Generated Angel on {}  is : {} ° or {} % of the expected angel {} ° ".format(date1,angle1,int((angle1/e_ang)*100),e_ang)
                b=" Generated Angel on {}  is : {} ° or {} % of the expected angel {} ° ".format(date2,angle2,int((angle2/e_ang)*100),e_ang)
                c=" Overall improvement is: {} %".format(abs(int((angle2/e_ang)*100)-int((angle1/e_ang)*100)))
                st.write(a)
                st.write(b)
                st.write("##"+c)
                st.markdown(gr.get_report(userdata[2],userdata[5],userdata[3]+" ( "+userdata[4]+") ","Contact: "+userdata[6]+"/ "+userdata[7],pname,sp,choiceS,page,pcontact,detection_on,[a,b,c],imagepath), unsafe_allow_html=True)
        except Exception as e:
            st.write("Something Went Wrong!")
            print(e)

    else:
        st.write("Upload an image")
