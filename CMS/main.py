# import the necessary packages
# local packages
from detection import detect
from utilities import triangulate, navigate, draw_vtm, draw_pts, draw_bot, draw_rts, display_msg, remove_vtm
import mqtt_router
# global packages
import numpy as np
import cv2
import time
import requests

from multiprocessing.dummy import Pool


# functions
def on_exit():
    # TODO - add on exit event logic
    mqtt_router.client.loop_stop()


# write the actual logic here
if __name__ == '__main__':
    # TODO - add logic
    pass
