import cv2 as cv
import sys
import numpy as np
from aruco_pos_finder import *
import Bots
import Inducts
import mqtt_router

# camera initialise
cap = cv.VideoCapture(0)
cap.set(4, 1080)
cap.set(3, 1920)

#ArUco variables init
dictionary = cv.aruco.Dictionary_get(cv.aruco.DICT_6X6_1000)

def rescaleFrame(frame, scale=0.7):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width, height)
    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

# Dictionary to store the ids and coordinates
Point = dict()
# Confirmation Loop
while True:
    ret, frm = cap.read()

    w = cv.waitKey(1) & 0xff

    if w == ord('c'):
            print(Point)
            fr = frm.copy()
            cv.destroyAllWindows()
            break

    if w == ord('q'):
        cap.release()
        cv.destroyAllWindows()
        sys.exit()

    parameters = cv.aruco.DetectorParameters_create()
    # Detect the markers in the image
    markerCorners, markerIds, rejectedCandidates = cv.aruco.detectMarkers(
        frm, dictionary, parameters=parameters)
    if (markerIds is not None):
        
        for a in markerIds:
            cc = np.where(markerIds == a[0])
            c = int(cc[0][0])
            s = str(Inducts.get(a[0]))
            x = int(markerCorners[c][0][0][0])
            y = int(markerCorners[c][0][0][1])
            cv.putText(frm,
                    s, (x, y),
                    cv.FONT_HERSHEY_PLAIN,
                    1, (255, 0, 255),
                    thickness=1)
            center = ((x + int(markerCorners[c][0][2][0])) // 2), ((y + int(markerCorners[c][0][2][1])) // 2)
            cv.circle(frm, center, 4, (0, 0, 255), -1)
            Point[a[0]] = center

        cv.aruco.drawDetectedMarkers(frm, markerCorners)
    cv.putText(frm,
               "Press 'c' to capture or 'q' to exit!",
               (10, 50),
               cv.FONT_HERSHEY_PLAIN,
               1.7, (255, 0, 255),
               thickness=2)
    cv.imshow("Choose your frame", rescaleFrame(frm))



# ArUco Detection
parameters =  cv.aruco.DetectorParameters_create()
# Detect the markers in the image
markerCorners, markerIds, rejectedCandidates = cv.aruco.detectMarkers(fr , dictionary, parameters=parameters)
if(markerIds is not None):
    for a in markerIds:
        cc = np.where(markerIds == a[0])
        c = int(cc[0][0])
        s = str(Inducts.get(a[0]))
        x = int(markerCorners[c][0][0][0])
        y = int(markerCorners[c][0][0][1])
        cv.putText(fr , s , (x,y) , cv.FONT_HERSHEY_PLAIN , 1 , (255 , 0 , 255) , thickness=1)
        c = c+1


cv.aruco.drawDetectedMarkers(fr , markerCorners)
cv.putText(fr,
            "Press 'R' to start execution!",
            (10, 50),
            cv.FONT_HERSHEY_PLAIN,
            2.5, (255, 0, 255),
            thickness=2)
cv.imshow('Image', rescaleFrame(fr))
cv.waitKey(0)
cv.destroyAllWindows()
# flags initialisation
print("Code Starts")
# while loop

cap.release()
cv.destroyAllWindows()
