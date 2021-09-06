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
def video_recorder(a, b):
    recorder = cv2.VideoWriter("Monochrome_Grid_3.0.mp4", cv2.VideoWriter_fourcc(*'MP4V'), 30.0, (a, b))
    return recorder

# functions
def on_exit():
    # TODO - add on exit event logic
    cap.release()
    cv2.destroyAllWindows()
    mqtt_router.client.loop_stop()
    sys.exit()


def mask_alternate(hsv_frame, lower, upper):     #alternate hard coded frame generator for contour calc
    mask = cv2.imread('images/mask.png', 0)  #must be specified
    calibrate = cv2.imread('images/calibrate.png', 0)  #must be specified
    frame = cv2.bitwise_and(hsv_frame, hsv_frame, mask=mask)
    thresh = cv2.inRange(frame, lower, upper)
    thresh = cv2.erode(thresh, None, iterations=1)
    thresh = cv2.dilate(thresh, None, iterations=1)
    return thresh

# write the actual logic here
if __name__ == '__main__':
    try:
        while cap.isOpened():
            ret, frame = cap.read()
            
            #updating recoder params
            height, width, _ = frame.shape
            record_v = video_recorder(height, width)
            
            #record_v.write(frame) #if recoding needed for basic image, can also be called to record the processed image only
            hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            # realtime mask made using object detector, can be hard coded too..
            mask_obj_detector = object_detector.apply(frame)
            ret, mask = cv2.threshold(mask_obj_detector, 200, 220, cv2.THRESH_BINARY)  # int values to be calibrated

            #alternate
            #lower = array([4, 113, 179])   #lower hsv space of obj colour
            #upper = array([129, 230, 237])   #upper hsv space of obj colour
            #mod_frame = mask_alternate(hsv_frame, lower, upper)

            #use mod_frame in place of mask if object_detector fails
            contours, h = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # edge points returned

            # optional exit call for testing
            if cv2.waitKey(10) & 0xFF == ord('e'):  # exit on "E" keypress
                break
        on_exit()


    except:
        print("Camera not working....calling on_exit!!!!")
        on_exit()
