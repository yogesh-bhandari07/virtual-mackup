import cv2
import imutils
import time
import dlib
import numpy as np
from makeup import makeup

detector = dlib.get_frontal_face_detector()
face_pose_predictor = dlib.shape_predictor("./data/shape_predictor_68_face_landmarks.dat")

'''
Getting Error because be detect only frontface ( detector = dlib.get_frontal_face_detector() )
'''


class VideoCamera(object):
    def __init__(self):
        # self.camera = "http://192.168.43.91:8080/video" # for access other device camera
        
        self.video = cv2.VideoCapture(0)      
        time.sleep(2.0) # use for preparing hardware

    def __del__(self):
        self.video.release()
        
        
    
    def get_frame(self,r,g,b):
        ret, frame = self.video.read()
        r=int(r)
        g=int(g)
        b=int(b)

        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        detected_faces = detector(gray, 0) # Face keypoints
        m = makeup(frame)

        for i, face_rect in enumerate(detected_faces):
            if not detected_faces:
                continue
            else:
                pose_landmarks = face_pose_predictor(gray, face_rect)

                landmark = np.empty([68, 2], dtype=int)
                for i in range(68):
                    landmark[i][0] = pose_landmarks.part(i).x
                    landmark[i][1] = pose_landmarks.part(i).y
                frame = m.apply_makeup(landmark, r, g, b)
            # frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)                                           
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()
