import cv2
import numpy
import mediapipe as mp
import pose_module as pm

cap = cv2.VideoCapture("/Users/dnymac/PycharmProjects/pose_detection/videos/demo2.mp4")
detector=pm.poseDetector()
while True:
    success,img=cap.read()
    img_get=detector.find_pos(img,False)
    lm_list=detector.find_landmark(img,False)
    try:
        if len(lm_list) !=0:
            # right arm
            ang=detector.find_angel(img,12,14,16)
            # right leg
            #ang = detector.find_angel(img, 24, 26, 28)
    except:
        pass
    cv2.imshow('Output', img_get)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
