import cv2
import mediapipe as mp
import math
import os


class poseDetector():
    def __init__(self, mode= True,segment=False, smooth= False, detectionCon=0.4, trackCon=0):
        self.mode=mode
        self.segment=segment
        self.smooth=smooth
        self.detectionCon=detectionCon
        self.trackingCon=trackCon
        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode,1,self.smooth,self.segment,False,self.detectionCon,self.trackingCon)
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
    def find_angel(self,img,p1,p2,p3,pos,draw=True):
        #get locations
        _, x1, y1  =self.landmark[p1]
        _, x2, y2 = self.landmark[p2]
        _, x3, y3 = self.landmark[p3]
        #calculate angel
        angel=abs(math.degrees(math.atan2(y3-y2,x3-x2)-math.atan2(y1-y2,x1-x2)))
        ## Different pose pre processing
        if pos == 1:
            angel = 180 - angel

        #########################

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



def main():
    path = os.getcwd() + "/videos/" + "img2.jpeg"
    write_path = os.getcwd() + "/predicted_output/" + "img2.jpg"
    cap = cv2.imread(path, 1)
    print(cap.shape)
    output = poseDetector.find_pos(cap, True)
    cv2.imwrite(write_path, output)
    cv2.imshow('Output', output)
    cv2.waitKey(0)

if __name__ == '__main__':
    main()
