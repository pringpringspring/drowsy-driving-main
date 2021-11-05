from scipy.spatial import distance as dist
from imutils.video import FileVideoStream
from imutils.video import VideoStream
from imutils import face_utils
import numpy as np
import argparse
import imutils
import time
import dlib
import cv2
import sys
from pyfirmata import Arduino, util
from socket import *

HOST = '192.168.219.108'
PORT = 5555
BUFSIZE = 1024
ADDR = (HOST,PORT)

clientSocket = socket(AF_INET, SOCK_STREAM)
board = Arduino('/dev/ttyACM0')


def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])

    ear = (A + B) / (2.0 * C)

    return ear

EYE_AR_THRESH = 0.2
EYE_AR_CONSEC_FRAMES = 15


COUNTER = 0
TOTAL = 0

print("Facial landmark predictor")
detector  = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")


(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

print("Starting Video Stream... ")
vs = VideoStream(usePiCamera=True).start()
time.sleep(1.0)

while True:
    frame = vs.read()
    frame = imutils.resize(frame, width = 450)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    rects = detector(gray, 0)

    for rect in rects:
        shape = predictor(gray,rect)
        shape = face_utils.shape_to_np(shape)

        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)

        ear = (leftEAR + rightEAR) /2.0

        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        cv2.drawContours(frame, [leftEyeHull], -1 , (0, 255, 0) , 1)
        cv2.drawContours(frame, [rightEyeHull], -1 , (0, 255, 0) , 1)

        
        if ear < EYE_AR_THRESH:
            COUNTER += 1

 	    if COUNTER >= EYE_AR_CONSEC_FRAMES:
		board.digital[13].write(1)
		

            cv2.putText(frame, "Alert" ,(10,30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255),2)
            try:
                clientSocket.connect(ADDR)
                clientSocket.send('START'.encode())
            except Exception as e:
                print('%s:%s'%ADDR)
                #sys.exit()
            print('Connect')
                

        else:
            COUNTER = 0
            board.digital[13].write(0)
	   


        cv2.putText(frame, "EAR: {:.3f} ".format(ear),(300,30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255),2)


    cv2.imshow("video" ,frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
         break

cv2.destroyAllWindows()
vs.stop()
