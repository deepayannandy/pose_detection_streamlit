import cv2
import mediapipe as mp
import os

mpDraw= mp.solutions.drawing_utils
mpPose= mp.solutions.pose
pose= mpPose.Pose()

path=os.getcwd()+"/sampel_images/"+"img4.jpeg"
write_path=os.getcwd()+"/predicted_output/"+"img4.jpeg"
print(path)
cap= cv2.imread(path)
imgRGB= cv2.cvtColor(cap,cv2.COLOR_BGR2RGB)
reasults=pose.process(imgRGB)
if reasults.pose_landmarks:
    mpDraw.draw_landmarks(cap,reasults.pose_landmarks,mpPose.POSE_CONNECTIONS)
    for id, lm in enumerate(reasults.pose_landmarks.landmark):
        h,w,c,=cap.shape
        print(id,lm)
        cx,cy =int(lm.x*w), int(lm.y*h)
        cv2.circle(cap,(cx,cy),6,(255,0,255),cv2.FILLED)
 
cv2.imwrite(write_path,cap)
cv2.imshow('Output',cap)
cv2.waitKey(0)

