import cv2
from numpy import *
import sys


def callback(x):
    pass


cap = cv2.VideoCapture(0)
cv2.namedWindow("HSV_Trackbars")

# range of Hue= 0-179, range of Saturation and Value = 0-255
cv2.createTrackbar("L_H", "HSV_Trackbars", 0, 179, callback)
cv2.createTrackbar("L_S", "HSV_Trackbars", 0, 255, callback)
cv2.createTrackbar("L_V", "HSV_Trackbars", 0, 255, callback)
cv2.createTrackbar("U_H", "HSV_Trackbars", 179, 179, callback)
cv2.createTrackbar("U_S", "HSV_Trackbars", 255, 255, callback)
cv2.createTrackbar("U_V", "HSV_Trackbars", 255, 255, callback)

def hsv_space_detector():
    try:
        while cap.isOpened():
            ret, rgb_frame = cap.read()
            hsv_frame = cv2.cvtColor(rgb_frame, cv2.COLOR_BGR2HSV)

            lower_hue = cv2.getTrackbarPos("L_H", "HSV_Trackbars")
            lower_saturation = cv2.getTrackbarPos("L_S", "HSV_Trackbars")
            lower_value = cv2.getTrackbarPos("L_V", "HSV_Trackbars")
            upper_hue = cv2.getTrackbarPos("U_H", "HSV_Trackbars")
            upper_saturation = cv2.getTrackbarPos("U_S", "HSV_Trackbars")
            upper_value = cv2.getTrackbarPos("U_V", "HSV_Trackbars")

            lower_range = array([lower_hue, lower_saturation, lower_value])
            upper_range = array([upper_hue, upper_saturation, upper_value])

            mask = cv2.inRange(hsv_frame, lower_range, upper_range)
            res = cv2.bitwise_and(rgb_frame, rgb_frame, mask=mask)
            mask_3 = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

            stack = hstack((mask_3, rgb_frame, res))
            cv2.imshow('Trackbars', cv2.resize(stack, None, fx=0.4, fy=0.4))

            if cv2.waitKey(1) & 0xFF == ord('q'):  # exit on "Q" keypress
                upper_lower_array = array([[lower_hue, lower_saturation, lower_value], [upper_hue, upper_saturation, upper_value]])
                print(upper_lower_array)
                return upper_lower_array
                break
        cap.release()
        cv2.destroyAllWindows()
    except:
        print("Camera not working...stopping execution")
        sys.exit()

#var = hsv_space_detector()
#print(var)
