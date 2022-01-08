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
    strt_pnts_coords = id_storage()
    end_pnts_coords = id_storage()

    # t_strt, t_end, i, j = 0, 0, 0, 0

    try:
        markerCorners, markerIds, rejectedCandidates = cv2.aruco.detectMarkers(frame, dictionary, parameters=parameters)
        for [ids] in markerIds:
            if len(strt_pnts_coords) == 4 and len(end_pnts_coords) == 4:
                break
            elif ids in range(680, 685):
                x, y = int(markerCorners[0][0][0][0] + markerCorners[0][0][2][0]) // 2, int(
                    markerCorners[0][0][0][1] + markerCorners[0][0][2][1]) // 2
                end_pnts_coords[ids] = tuple(x, y)
            elif ids in range(830, 835):
                x, y = int(markerCorners[0][0][0][0] + markerCorners[0][0][2][0]) // 2, int(
                    markerCorners[0][0][0][1] + markerCorners[0][0][2][1]) // 2
                strt_pnts_coords[ids] = tuple(x, y)
            else:
                continue

        return strt_pnts_coords, end_pnts_coords

    except:
        time.sleep(0.25)
        markerCorners, markerIds, rejectedCandidates = cv2.aruco.detectMarkers(frame, dictionary, parameters=parameters)
        for [ids] in markerIds:
            if len(strt_pnts_coords) == 4 and len(end_pnts_coords) == 4:
                break
            elif ids in range(680, 685):
                x, y = int(markerCorners[0][0][0][0] + markerCorners[0][0][2][0]) // 2, int(
                    markerCorners[0][0][0][1] + markerCorners[0][0][2][1]) // 2
                end_pnts_coords[ids] = tuple(x, y)
            elif ids in range(830, 835):
                x, y = int(markerCorners[0][0][0][0] + markerCorners[0][0][2][0]) // 2, int(
                    markerCorners[0][0][0][1] + markerCorners[0][0][2][1]) // 2
                strt_pnts_coords[ids] = tuple(x, y)
            else:
                continue

        return strt_pnts_coords, end_pnts_coords

    finally:
        print("No frame provided even after waiting")
        return 0, 0   #for inclusion in main, if return values are 0 rerun process
        #sys.exit()
    
