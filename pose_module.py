import cv2
import mediapipe as mp
import math
import os


class poseDetector():
    def __init__(self, mode= False,segment=False, smooth= True, detectionCon=0.5, trackCon=0.5):
        self.mode=mode
        self.segment=segment
        self.smooth=smooth
        self.detectionCon=detectionCon
        self.trackingCon=trackCon
        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode,1,self.smooth,self.segment,True,self.detectionCon,self.trackingCon)
    def find_pos(self,img,draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.reasults = self.pose.process(imgRGB)
        if self.reasults.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.reasults.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
        return img
    def find_landmark(self,img,draw=True):
        self.landmark=[]
        try:
            for id, lm in enumerate(self.reasults.pose_landmarks.landmark):
                h, w, c, = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.landmark.append([id,cx,cy])
                if draw:
                    cv2.circle(img, (cx, cy), 6, (255, 0, 255), cv2.FILLED)
            return self.landmark
        except:
            pass
    def find_angel(self,img,p1,p2,p3,draw=True):
        #get locations
        _, x1, y1  =self.landmark[p1]
        _, x2, y2 = self.landmark[p2]
        _, x3, y3 = self.landmark[p3]
        #calculate angel
        angel=math.degrees(math.atan2(y3-y2,x3-x2)-math.atan2(y1-y2,x1-x2))
        if angel < 0:
            angel += 360
        #draw angel
        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 4)
            cv2.line(img, (x2, y2), (x3, y3), (0, 255, 0), 4)
            cv2.circle(img, (x1, y1), 6, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x1, y1), 12, (255, 0, 0), 2)
            cv2.circle(img, (x2, y2), 6, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x2, y2), 12, (255, 0, 0), 2)
            cv2.circle(img, (x3, y3), 6, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x3, y3), 12, (255, 0, 0), 2)

            cv2.putText(img, str(int(angel)), (x2 - 50, y2 + 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        return angel



def main(file_name):
    cap = cv2.VideoCapture(file_name)
    detector=poseDetector()
    while True:
        success,img=cap.read()
        if success:
            img_get=detector.find_pos(img)
            lm_list=detector.find_landmark(img)
            print(lm_list[14])
        else:
            pass
        cv2.imshow('Output', img_get)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main("/Users/dnymac/PycharmProjects/pose_detection/videos/demo1.mp4")
