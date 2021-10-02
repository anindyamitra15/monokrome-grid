import cv2 as cv
import sys
import numpy as np
import Bots
import Inducts
from mqtt_router import control, on_exit
import utils

# camera initialise
frame_timing = 1 # in milliseconds
cap = cv.VideoCapture(0, cv.CAP_DSHOW)
cap.set(cv.CAP_PROP_FPS, 30.0)
cap.set(cv.CAP_PROP_FOURCC, cv.VideoWriter.fourcc('m', 'j', 'p', 'g'))
cap.set(cv.CAP_PROP_FOURCC, cv.VideoWriter.fourcc('M', 'J', 'P', 'G'))
cap.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 720)

#ArUco variables init
dictionary = cv.aruco.Dictionary_get(cv.aruco.DICT_6X6_1000)
parameters = cv.aruco.DetectorParameters_create()

#Globals
Induct_Dist_Thres = 20
Bot_Angle_Thres = 20
Speed_pwm = 200
Pro_con = 0.5


def rescaleFrame(frame, scale=1):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width, height)
    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

# Dictionary to store the ids and coordinates
Point = dict()
# Arena confirmation Loop
# Loop 1
#xys = set()
while True:
    ret, frm = cap.read()

    w = cv.waitKey(frame_timing) & 0xff

    if w == ord('q'):
        cap.release()
        cv.destroyAllWindows()
        on_exit()
        sys.exit()

    # Detect the markers in the image
    markerCorners, markerIds, rejectedCandidates = cv.aruco.detectMarkers(frm, dictionary, parameters=parameters)
    if (markerIds is not None):
        for a in markerIds:
            cc = np.where(markerIds == a[0])
            c = int(cc[0][0])
            s = str(Inducts.get_name(a[0]))
            Point[a[0]] = utils.find_coordinates(markerCorners, c)
            (x,y) = Point[a[0]][1]
            cv.putText(frm,
                    s, (x, y),
                    cv.FONT_HERSHEY_PLAIN,
                    1, (255, 0, 255),
                    thickness=1)
            center = Point[a[0]][0]
            cv.circle(frm, center, 4, (0, 0, 255), -1)


        # Logic for showing paths
        if set(Inducts.SD.keys()).issubset(Point.keys()):
            for i in range(0, 4):
                S = Point[Inducts.key_list[i]][0] # S point
                D = Point[Inducts.key_list[i+4]][0] # D point
                M = (S[0], D[1]) # Mid point
                #xys.add(M)
                cv.circle(frm, M, 4, (0, 0, 255), -1)
                cv.line(frm, S, M, (164, 73, 163), 2)
                cv.line(frm, D, M, (164, 73, 163), 2)

        cv.aruco.drawDetectedMarkers(frm, markerCorners)

        if w == ord('c'):
            print(Point)
            fr = frm.copy()
            cv.destroyAllWindows()
            break

    cv.putText(frm,
               "Press 'c' to capture or 'q' to exit!",
               (10, 50),
               cv.FONT_HERSHEY_PLAIN,
               1.7, (255, 0, 255),
               thickness=2)
    cv.imshow("Choose your frame", rescaleFrame(frm))

# Confirmation Snapshot
cv.putText(fr,
            "Press any key, after you have placed all the bots!",
            (10, 50),
            cv.FONT_HERSHEY_PLAIN,
            2.5, (255, 0, 255),
            thickness=2)
cv.imshow('Image', rescaleFrame(fr))
cv.waitKey(0)
cv.destroyAllWindows()

# To detect the bot positions on Source inducts
Location = dict()
# Loop 2
while True:
    ret, frm = cap.read()

    if cv.waitKey(frame_timing) & 0xff == ord('p'):
        print(Point)
        break

    # Detect the markers in the image
    markerCorners, markerIds, rejectedCandidates = cv.aruco.detectMarkers(
        frm, dictionary, parameters=parameters)
    if (markerIds is not None):
        for a in markerIds:
            cc = np.where(markerIds == a[0])
            c = int(cc[0][0])
            s = str(Inducts.get_name(a[0]))
            Point[a[0]] = utils.find_coordinates(markerCorners, c)
            (x, y) = Point[a[0]][1]
            cv.putText(frm,
                       s, (x, y),
                       cv.FONT_HERSHEY_PLAIN,
                       1, (255, 0, 255),
                       thickness=1)
            center = Point[a[0]][0]
            cv.circle(frm, center, 4, (0, 0, 255), -1)

        for k in Bots.key_list:
            if k in Point.keys():
                center = Point[k][0]
                for l in range(0, 4):
                    id = Inducts.key_list[l]
                    coordinates = Point[id]
                    if center[0] in range(coordinates[1][0], coordinates[2][0]):
                        Location[id] = Bots.get_id(k)

    cv.putText(frm, "Press 'p' to start execution!",
            (10, 50),
            cv.FONT_HERSHEY_PLAIN,
            2.5, (255, 0, 255),
            thickness=2)
    cv.aruco.drawDetectedMarkers(frm, markerCorners)
    cv.imshow("Frame", rescaleFrame(frm))
print("Locations")
print(Location) # GGGGGGGGGGGGGGGGGGGGGGGGGGGGG

# on_exit()
# sys.exit()
# flags initialisation
n:int = 0
err_flag = False
isVertical = True
isReturn = False
pwm_r = Speed_pwm
pwm_l = Speed_pwm
pwm_b = Speed_pwm
while True:
    ret, frm = cap.read()

    Sx = Inducts.key_list[n] # ArUco for Source Induct
    Dx = Inducts.key_list[n + 4]  # ArUco for destination Induct
    S_cnt = Point[Sx][0] # center point of source induct
    D_cnt = Point[Dx][0]  # center point of destination induct
    # exit sequence
    if cv.waitKey(1) & 0xff == ord('q') or n >= 4 or Sx not in Location.keys():
        for ids in Bots.val_list:
            control(ids, 3, direction = 0, pwm = 0)
        break
    id = Location[Sx] # get the bot Id placed on the particular source induct
    num = Bots.get_num(id) # ArUco number of that bot

    # Detect the markers in the image
    markerCorners, markerIds, rejectedCandidates = cv.aruco.detectMarkers(frm, dictionary, parameters=parameters)
    if (markerIds is not None):
        for a in markerIds:
            cc = np.where(markerIds == a[0])
            c = int(cc[0][0])
            if a[0] == num: # if the detected id is the bot of interest
                cofbot, left_top, _ = utils.find_coordinates(markerCorners, c)
                s = str(Bots.get_id(a[0]))
                cv.putText(frm, s, left_top, cv.FONT_HERSHEY_PLAIN, 1, (255, 0, 255), thickness=2)
                cv.circle(frm, cofbot, 2, (0, 0, 255), -1)
                right_top = int(markerCorners[c][0][1][0]), int(markerCorners[c][0][1][1])
                fofbot = utils.mid_pt(left_top, right_top)
                cv.arrowedLine(frm, cofbot, fofbot, (50,255,128), 2)
                mid = utils.std_v(S_cnt, D_cnt)
                if isVertical and not isReturn:
                    normal = utils.std_v(S_cnt, cofbot)
                    dist_normal = utils.dist(cofbot, normal)
                    cv.line(frm, cofbot, normal, (255, 0, 0), 2)
                    dist_dest = utils.dist(cofbot, mid) # dist. from bot to turn point
                    _, angle = utils.anglechecker(cofbot, fofbot, mid)
                    #Bot should move forward
                    control(id , 3 , direction =1) 

                    x2 = cofbot[0]   
                    x1 = S_cnt[0]

                    if x2 - x1> 0:
                        print("Left higher")
                        control(id,1, pwm=pwm_l+Pro_con*dist_normal)

                    elif x2 - x1 < 0:
                        print("Right higher")
                        control(id, 2, pwm=pwm_r + Pro_con * dist_normal)

                    if dist_dest < Induct_Dist_Thres:
                        isVertical = False   #eikhane ekta control(id, 3, direction=0)

                        #isVertical ke if else er moddhe dhukiye False kor
                        if 0 <= n <= 1:
                            print("Bot turns right")
                            control(id,2, direction=1,pwm=pwm_r)
                            control(id,1, direction=2,pwm=pwm_l)
                        else:
                            print("Bot turns left")
                            control(id,1, direction=1,pwm=pwm_r)
                            control(id,2, direction=2,pwm=pwm_l)

                # end of vertical f6rward locomotion scope
                elif not isVertical and not isReturn:
                    normal = utils.std_h(D_cnt, cofbot)
                    cv.line(frm, cofbot, normal, (255, 0, 0), 2)
                    dist_dest = utils.dist(cofbot, D_cnt)  # dist. from bot to turn point
                    _, angle = utils.anglechecker(cofbot, fofbot, D_cnt)
                    
                    if (angle < Bot_Angle_Thres and dist_normal < Induct_Dist_Thres):
                        print("Bot moves forward")
                        control(id, 3, direction=0)
                        
                    if dist_dest < Induct_Dist_Thres:
                        isReturn = True
                        print("Bot unloads")
                        print("Bot comes back gear")
                # end of horizontal forward locomotion scope
                elif not isVertical and isReturn:
                    normal = utils.std_h(D_cnt, cofbot)
                    cv.line(frm, cofbot, normal, (255, 0, 0), 2)
                    dist_dest = utils.dist(cofbot, mid)
                    _, angle = utils.anglechecker(cofbot, fofbot, mid)
                    if dist_dest < Induct_Dist_Thres:
                        isVertical = True
                        if 0 <= n <= 1:
                            print("Bot turns right")
                        else:
                            print("Bot turns left")
                        print("Bor moves forward")
                # end of horizontal return locomotion scope
                elif isVertical and isReturn:
                    normal = utils.std_v(S_cnt, cofbot)
                    cv.line(frm, cofbot, normal, (255, 0, 0), 2)
                    dist_dest = utils.dist(cofbot, S_cnt)
                    _, angle = utils.anglechecker(cofbot, fofbot, S_cnt)
                    if dist_dest < Induct_Dist_Thres:
                        isReturn = False
                        print("Bot stops")
                        print(n)
                        n += 1
                        pwm_r = Speed_pwm
                        pwm_l = Speed_pwm
                        pwm_b = Speed_pwm
                        print("goes to ")
                        print(n)
                # end of vertical return locomotion scope





    cv.aruco.drawDetectedMarkers(frm, markerCorners)
    cv.imshow("Frame", rescaleFrame(frm))


cap.release()
cv.destroyAllWindows()
