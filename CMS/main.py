# import the necessary packages
# local packages
from detection import detect
from utilities import triangulate, navigate, draw_vtm, draw_pts, draw_bot, draw_rts, display_msg, remove_vtm
import mqtt_router
# global packages
from numpy import *
import cv2
import time
import requests
import sys

from multiprocessing.dummy import Pool

cap = cv2.VideoCapture(0)


class Flags:
    def __init__(self):
        self.Start = True
        self.Mid = False
        self.Drop = False
        self.Return = False
        self.End = False
        self.Straight = True


object_detector = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=40)


# functions
def on_exit():
    # TODO - add on exit event logic
    cap.release()
    cv2.destroyAllWindows()
    mqtt_router.client.loop_stop()
    sys.exit()


# write the actual logic here
if __name__ == '__main__':
    try:
        while cap.isOpened():
            ret, frame = cap.read()
            hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            # realtime mask made using object detector, can be hard coded too..
            mask_obj_detector = object_detector.apply(frame)
            ret, mask = cv2.threshold(mask_obj_detector, 200, 220, cv2.THRESH_BINARY)  # int values to be calibrated
            contours, h = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # edge points returned

            # optional exit call for testing
            if cv2.waitKey(10) & 0xFF == ord('e'):  # exit on "E" keypress
                break
        on_exit()


    except:
        print("Camera not working....calling on_exit!!!!")
        on_exit()
