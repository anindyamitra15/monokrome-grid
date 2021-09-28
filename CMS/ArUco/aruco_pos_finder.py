#4 dim arrays
import cv2
import time
import sys

#ids ar 2d arrays
#might be req to take the below part within the function
dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_1000)
parameters = cv2.aruco.DetectorParameters_create()
#upto here

def id_fetcher_initial(frame):  #run initially to fetch start and end points
    start_point_coords = []
    end_point_coords = []
    t_strt = 0
    t_end = 0
    try:
        markerCorners, markerIds, rejectedCandidates = cv2.aruco.detectMarkers(frame, dictionary, parameters=parameters)
        for [ids] in markerIds:
            if t_strt == 4 and t_end == 4:
                break
            else:
                if ids in range(680, 685):  #D1, D2, D3, D4
                    x, y = (markerCorners[0][0][0][0] + markerCorners[0][0][2][0]) // 2, (markerCorners[0][0][0][1] + markerCorners[0][0][2][1]) // 2
                    end_point_coords.append(tuple(x, y))   #centre coords
                    t_strt += 1
                elif ids in range(830, 835):   #S1, S2, S3, S4
                    x, y = (markerCorners[0][0][0][0] + markerCorners[0][0][2][0]) // 2, (markerCorners[0][0][0][1] + markerCorners[0][0][2][1]) // 2
                    start_point_coords.append(tuple(x, y))  #centre coords
                    t_end += 1
                else:
                    print("Wrong id detected")
        return start_point_coords, end_point_coords  #returning an array containing (x, y) of start and end points

    except:
        time.sleep(0.25)  #code will sleep for this amount of secs if frame not found
        markerCorners, markerIds, rejectedCandidates = cv2.aruco.detectMarkers(frame, dictionary, parameters=parameters)
        for [ids] in markerIds:
            if t_strt == 4 and t_end == 4:
                break
            else:
                if ids in range(680, 685):  # D1, D2, D3, D4
                    x, y = (markerCorners[0][0][0][0] + markerCorners[0][0][2][0]) // 2, (
                                markerCorners[0][0][0][1] + markerCorners[0][0][2][1]) // 2
                    end_point_coords.append(tuple(x, y))  # centre coords
                    t_strt += 1
                elif ids in range(830, 835):  # S1, S2, S3, S4
                    x, y = (markerCorners[0][0][0][0] + markerCorners[0][0][2][0]) // 2, (
                                markerCorners[0][0][0][1] + markerCorners[0][0][2][1]) // 2
                    start_point_coords.append(tuple(x, y))  # centre coords
                    t_end += 1
                else:
                    print("Wrong id detected")
        return start_point_coords, end_point_coords  # returning an array containing (x, y) of start and end points
    finally:
        print("no frame found after waiting")
        sys.exit()
