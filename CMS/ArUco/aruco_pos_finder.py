# 4 dim arrays
import cv2
import time
import sys

# ids ar 2d arrays
# might be req to take the below part within the function
dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_1000)
parameters = cv2.aruco.DetectorParameters_create()
# upto here

class id_storage(dict):
    def __init__(self):
        self = dict()

    def element_adder(self, key, value):
        self[key] = value


#rewrote using dictionary and updated logic so as duplicate values for same ids don't cause trouble
#it will return 2 dicts, with keys as id number and values as their centre coords
def id_fetcher_initial(frame):
    coords = id_storage()

    markerCorners, markerIds, rejectedCandidates = cv2.aruco.detectMarkers(frame, dictionary, parameters=parameters)
    for [ids] in markerIds:
        
            x, y = int(markerCorners[0][0][0][0] + markerCorners[0][0][2][0]) // 2, int(
                markerCorners[0][0][0][1] + markerCorners[0][0][2][1]) // 2
            coords[ids] = (x, y)

    return coords


if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    while True:
        ret, frm = cap.read()
        dict1 = id_fetcher_initial(frm)
        print("DDDDDDIIIIICCCCTTTTTT 1")
        print(dict1)
        cv2.imshow("f", frm)
        if cv2.waitKey(1) & 0xff == ord('n'):
            break

    cap.release()
    cv2.destroyAllWindows()
