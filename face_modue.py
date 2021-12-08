import cv2
import mediapipe as mp
import time
import os



class FaceMeshDetector():
    def __init__(self,static_image_mode = False,max_num_faces = 1,refine_landmarks = True,min_detection_confidence = 0.8,min_tracking_confidence = 0.8):
        self.static_image_mode = static_image_mode
        self.max_num_faces = max_num_faces
        self.refine_landmarks = refine_landmarks
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence

        self.mpDraw = mp.solutions.drawing_utils
        self.mpFaceMesh = mp.solutions.face_mesh
        self.faceMesh = self.mpFaceMesh.FaceMesh(self.static_image_mode,self.max_num_faces,self.refine_landmarks,self.min_detection_confidence, self.min_tracking_confidence)
        self.drawSpec = self.mpDraw.DrawingSpec(thickness=1, circle_radius=1,color=[220, 220, 220])
        self.drawSpecL = self.mpDraw.DrawingSpec(thickness=4, circle_radius=1, color=[0, 255, 20])

    def findfaces(self,img, deaw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.landmarks = []
        self.results=self.faceMesh.process(imgRGB)
        if self.results.multi_face_landmarks:
            for facelandmarks in self.results.multi_face_landmarks:
                self.mpDraw.draw_landmarks(img, facelandmarks, self.mpFaceMesh.FACEMESH_LIPS,self.drawSpec,self.drawSpecL )

                for id, lm in enumerate(self.results.multi_face_landmarks[0].landmark):
                    h, w, c, = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    self.landmarks.append([id, cx, cy])

        return img, self.landmarks
    def find_distance(self,landmark):
        pass





def main():
    path = os.getcwd() + "/videos/" + "img2.jpeg"
    write_path = os.getcwd() + "/predicted_output/" + "img2.jpg"
    cap= cv2.imread(path,1)
    print(cap.shape)
    output=FaceMeshDetector.findfaces(cap,True)
    cv2.imwrite(write_path, output)
    cv2.imshow('Output', output)
    cv2.waitKey(0)

if __name__ == '__main__':
    main()