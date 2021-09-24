#code might not work on individual machines if opencv-contrib is not installed

import cv2 as cv
import numpy as np

# Load the dictionary that was used to generate the markers.
dictionary = cv.aruco.Dictionary_get(cv.aruco.DICT_6X6_250)
capture = cv.VideoCapture("Arena4Bot2Mov-ArUco.mp4")  #input your saved video/ webcam feed

#code basically merges aruco params obtained from hsv space and original img into a single frame
#gives better detection capability

def callback():
    pass

cv.namedWindow("HSV_Trackbars")
cv.resizeWindow("HSV_Trackbars", 500, 500)
# range of Hue= 0-179, range of Saturation and Value = 0-255
cv.createTrackbar("L_H", "HSV_Trackbars", 0, 179, callback)
cv.createTrackbar("L_S", "HSV_Trackbars", 0, 255, callback)
cv.createTrackbar("L_V", "HSV_Trackbars", 0, 255, callback)
cv.createTrackbar("U_H", "HSV_Trackbars", 179, 179, callback)
cv.createTrackbar("U_S", "HSV_Trackbars", 255, 255, callback)
cv.createTrackbar("U_V", "HSV_Trackbars", 255, 255, callback)


def rescaleFrame(frame, scale):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width, height)
    return cv.resize(frame, dimensions)

def hsv_space_finder():
    lower_hue = 0
    lower_saturation = 165
    lower_value = 74
    upper_hue = 179
    upper_saturation = 255
    upper_value = 255

    return np.array([lower_hue, lower_saturation, lower_value]), np.array([upper_hue, upper_saturation, upper_value])


while True:
    isTrue, frame = capture.read()
    if not isTrue:
        break
    # frame calibration
    frame = rescaleFrame(frame, 0.7)
    cv.imshow("Original", frame)

    frame_cnv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    #lower, upper = hsv_space_finder()
    cv.imshow("HSV Frame", frame_cnv)

    #mask = cv.inRange(frame_cnv, (0, 0, 254), (3, 3, 255))
    #mask = cv.erode(mask, None, iterations=2)
    #mask = cv.dilate(mask, None, iterations=2)

    #img = cv.bitwise_and(frame, frame, mask=mask)
    #cv.imshow('image_final', img)

    parameters = cv.aruco.DetectorParameters_create()
    # Detect the markers in the image
    markerCorners, markerIds, rejectedCandidates = cv.aruco.detectMarkers(frame, dictionary, parameters=parameters)
    markerCorners1, markerIds1, rejectedCandidates1 = cv.aruco.detectMarkers(frame_cnv, dictionary, parameters=parameters)
    #print(markerIds)
    # cc = np.where(markerIds == 0)
    # c = int(cc[0][0])
    # cv.rectangle(frame_resized , (int(markerCorners[c][0][0][0]) , int(markerCorners[c][0][0][1])) , (int(markerCorners[c][0][2][0]) , int(markerCorners[c][0][2][1])) , (0, 255 , 0) , thickness = 2)

    cv.aruco.drawDetectedMarkers(frame, markerCorners)
    cv.aruco.drawDetectedMarkers(frame, markerCorners1)
    cv.imshow("Detected", frame)

    # "2" se kaam nehi ho raha tha...usliye Q diya
    if cv.waitKey(1) & 0xFF == ord('q'):
        print("Keyboard interrupt")
        break
capture.release()
cv.destroyAllWindows()
