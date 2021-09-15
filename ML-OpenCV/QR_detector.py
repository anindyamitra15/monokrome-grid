import cv2
import numpy as np
from pyzbar.pyzbar import decode

global actual_data

def QR_Code_reader(actual_data=None):
    capture = cv2.VideoCapture(0)
    cv2.namedWindow("QR_Code_read_window", 0)
    cv2.resizeWindow("QR_Code_read_window", 1600, 900)
    if not capture.isOpened():
        print("Camera error")
    else:
        while True:
            failure, img = capture.read()
            for qrcode in decode(img):
                actual_data = qrcode.data.decode( 'utf-8')  # only data will be stored in actual_data var, actual QRCODE readings return many values including data
                #print(actual_data) #if data needs printing on console
                # bounding box code
                pts = np.array([qrcode.polygon], np.int32)
                pts = pts.reshape((-1, 1, 2))  # arbitary reshaping based on example
                cv2.polylines(img, [pts], True, (0, 255, 0),
                              2)  # Syntax: cv2.polylines(image, [pts], isClosed, color(RGB format), thickness)
                # for debugging purposes, if data readings is to be shown on screen
                pts1 = qrcode.rect
                cv2.putText(img, actual_data, (pts1[0], pts1[1]), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0),
                            1)  # Syntax: cv2.putText(image, text, org, font, fontScale, color, thickness, lineType, bottomLeftOrigin)
            cv2.imshow("Result: ", img)
            cv2.waitKey(100)  # in milisecs
    return actual_data

def Bot_id_checker(data, strings=None):
    id_lists = ["Monochrome", "Nebula", "LukeAnubis", "Valorant"]
    bot_no = 0
    for strings in id_lists and data == strings:
        bot_no = id_lists.index(strings)
        bot_no += 1
    print(bot_no)


print(QR_Code_reader(None))
#print(Bot_id_checker(a, None))
