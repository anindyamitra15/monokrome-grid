import cv2 as cv
import sys
import numpy as np
import Bots
import Inducts
from mqtt_router import control, on_exit
import utils

# camera initialise
frame_timing = 1  # in milliseconds
cap = cv.VideoCapture(0, cv.CAP_DSHOW)
cap.set(cv.CAP_PROP_FPS, 30.0)
cap.set(cv.CAP_PROP_FOURCC, cv.VideoWriter.fourcc('m', 'j', 'p', 'g'))
cap.set(cv.CAP_PROP_FOURCC, cv.VideoWriter.fourcc('M', 'J', 'P', 'G'))
cap.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 720)

# ArUco variables init
dictionary = cv.aruco.Dictionary_get(cv.aruco.DICT_6X6_1000)
parameters = cv.aruco.DetectorParameters_create()

# Globals
Induct_Dist_Thres = 20
Bot_Angle_Thres = 10
Speed_pwm = 400
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
# xys = set()
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
    if markerIds is not None:
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

        # Logic for showing paths
        if set(Inducts.SD.keys()).issubset(Point.keys()):
            for i in range(0, 4):
                S = Point[Inducts.key_list[i]][0]  # S point
                D = Point[Inducts.key_list[i + 4]][0]  # D point
                M = (S[0], D[1])  # Mid point
                # xys.add(M)
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
    if markerIds is not None:
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
print(Location)  # GGGGGGGGGGGGGGGGGGGGGGGGGGGGG

# on_exit()
# sys.exit()
# flags initialisation
n: int = 0
err_flag = False
isVertical = True
isReturn = False
forwarded = False
pwm_r = Speed_pwm
pwm_l = Speed_pwm
pwm_b = Speed_pwm
while True:
    ret, frm = cap.read()

    Sx = Inducts.key_list[n]  # ArUco for Source Induct
    Dx = Inducts.key_list[n + 4]  # ArUco for destination Induct
    S_cnt = Point[Sx][0]  # center point of source induct
    D_cnt = Point[Dx][0]  # center point of destination induct

    # exit sequence
    if cv.waitKey(1) & 0xff == ord('q') or n >= 4 or Sx not in Location.keys():
        for ids in Bots.val_list:
            control(ids, 3, direction=0, pwm=0)
        break
    id = Location[Sx]  # get the bot Id placed on the particular source induct
    num = Bots.get_num(id)  # ArUco number of that bot

    # Detect the markers in the image and begins the game
    markerCorners, markerIds, rejectedCandidates = cv.aruco.detectMarkers(frm, dictionary, parameters=parameters)
    # if marker Ids are found
    if markerIds is not None:
        # for each marker Ids
        for a in markerIds:
            cc = np.where(markerIds == a[0])
            c = int(cc[0][0])
            # if the detected id is the bot of interest
            if a[0] == num:
                # center of bot: cofbot
                # left_top gives left top corner point of bot
                cofbot, left_top, _ = utils.find_coordinates(markerCorners, c)
                s = str(Bots.get_id(a[0]))
                # puts the chip Id text on the bot of interest
                cv.putText(frm, s, left_top, cv.FONT_HERSHEY_PLAIN, 1, (255, 0, 255), thickness=2)
                # points the center on the image
                cv.circle(frm, cofbot, 2, (0, 0, 255), -1)
                # necessary for finding front-mid of bot
                right_top = int(markerCorners[c][0][1][0]), int(markerCorners[c][0][1][1])

                fofbot = utils.mid_pt(left_top, right_top) # front of bot
                # draws an arrow towards the front from center of bot
                cv.arrowedLine(frm, cofbot, fofbot, (50, 255, 128), 2)

                # mid gives the mid point of the track
                mid = utils.std_v(S_cnt, D_cnt) # vertical point of intersection (x1, y2)

                # not finite state approach starts in the master loop
                # scope 1: bot goes forward stops at mid
                if isVertical and not isReturn:
                    normal = utils.std_v(S_cnt, cofbot)  # point of the foot of perpendicular
                    # show a blue line from cofbot to foot
                    cv.line(frm, cofbot, normal, (255, 0, 0), 2)

                    dist_dest = utils.dist(cofbot, mid)  # dist. from bot to turn point
                    # angle between mid-cofbot-fofbot
                    _, angle = utils.anglechecker(cofbot, fofbot, mid)
                    # if the bot is on the induct
                    if not forwarded and utils.dist(cofbot, S_cnt) < Induct_Dist_Thres:
                        # instructs the bot to move fwd
                        control(id, 3, direction=1, pwm=Speed_pwm)
                        forwarded = True
                    # 'X' points of Normal foot and cofbot
                    x2 = cofbot[0]
                    x1 = normal[0]
                    dist_normal = x2 - x1  # normal distance of bot from the track in x axis with sign
                    # dumps the value
                    # print(dist_normal)

                    # scope 1 exitter section
                    if dist_dest < Induct_Dist_Thres:
                        isVertical = False # now horizontal block executes
                        forwarded = False
                        control(id, 3, direction=0) # stops the bot
                        print("Exiting scope 1")

                    # PID control begins
                    # PID left side increase bias
                    if (dist_normal > 0):
                        # print("Left higher")
                        control(id, 1, pwm=Speed_pwm + Pro_con * dist_normal)
                    # PID left side decrease bias
                    elif (dist_normal < 0):
                        # print("Left Lower")
                        control(id, 1, pwm=Speed_pwm + Pro_con * dist_normal)

                # end of vertical forward locomotion scope
                # scope 2: bot turns left or right depending on 0 <= n <= 1 or 2 <= n <= 3, bot moves forward to destination and unloads at destination
                elif not isVertical and not isReturn:
                    normal = utils.std_h(D_cnt, cofbot) # point of the foot of perpendicular
                    # show a blue line from cofbot to foot
                    cv.line(frm, cofbot, normal, (255, 0, 0), 2)
                    dist_dest = utils.dist(cofbot, D_cnt)  # dist. from bot to Destination
                    _, angle = utils.anglechecker(cofbot, fofbot, D_cnt)

                    y2 = cofbot[1]
                    y1 = normal[1]
                    dist_normal = y2 - y1  # normal distance of bot from the track in y axis with sign
                    # dumps the value
                    # print(dist_normal)

                    # if the bot is on mid
                    if not forwarded and utils.dist(cofbot, mid) < Induct_Dist_Thres:
                        # if the bot turned right and is ready to move fwd

                        #start turning the bot to the right for 0 <= n <= 1
                        print("Turning")
                        control(id, 3, direction=1, pwm=int(Speed_pwm//1.5))
                        if 0 <= n <= 1:
                            control(id, 2, direction=2)
                            print("Right")
                        elif 2 <= n <= 3:
                            print("Left")
                            control(id, 1, direction=2)
                        print(angle,dist_normal)
                        if abs(angle) < Bot_Angle_Thres and abs(dist_normal) < Induct_Dist_Thres: # new threshold
                            print("Bot is forwarded")
                            control(id, 3, direction=1, pwm=Speed_pwm)  # forwards the bot
                            forwarded = True

                    # scope 2 exitter section
                    if dist_dest < Induct_Dist_Thres:
                        isReturn = True
                        forwarded = False
                        control(id, 0, logic=True) # stops and unloads
                        print("End of scope 2")

                    # PID control begins
                    # PID left side increase bias
                    if (dist_normal > 0):
                        # print("Left higher")
                        control(id, 1, pwm=Speed_pwm + Pro_con * dist_normal)
                    # PID left side decrease bias
                    elif (dist_normal < 0):
                        # print("Left Lower")
                        control(id, 1, pwm=Speed_pwm + Pro_con * dist_normal)

                # end of horizontal forward locomotion scope
                # scope 3: bot moves backward, upto mid and stops at mid
                elif not isVertical and isReturn:
                    normal = utils.std_h(D_cnt, cofbot)
                    cv.line(frm, cofbot, normal, (255, 0, 0), 2)
                    dist_dest = utils.dist(cofbot, mid)
                    _, angle = utils.anglechecker(cofbot, fofbot, mid)

                    y2 = cofbot[1]
                    y1 = normal[1]
                    dist_normal = y2 - y1  # normal distance of bot from the track in y axis with sign
                    # dumps the value
                    # print(dist_normal)

                    # if the bot is on Destination
                    if not forwarded and utils.dist(cofbot, D_cnt) < Induct_Dist_Thres:
                        # if the bot turned right and is ready to move fwd
                        control(id, 3, direction=2, pwm=Speed_pwm)  # backward moves the bot
                        forwarded = True # backwarded

                    # scope 3 exitter section
                    if dist_dest < Induct_Dist_Thres:
                        isVertical = True
                        forwarded = False
                        control(id, 3, direction=0)

                    # PID control begins
                    # PID left side increase bias
                    if (dist_normal > 0):
                        # print("Left higher")
                        control(id, 1, pwm=Speed_pwm + Pro_con * dist_normal)
                    # PID left side decrease bias
                    elif (dist_normal < 0):
                        # print("Left Lower")
                        control(id, 1, pwm=Speed_pwm + Pro_con * dist_normal)

                # end of horizontal return locomotion scope
                # scope 4: bot turns right 90 for 0 <= n <= 1 or bot turns left 90 for 2 <= n <= 3
                # and stops at Source Induct
                # and shifts control to next bot
                # and initialises globals and flags
                elif isVertical and isReturn:
                    normal = utils.std_v(S_cnt, cofbot)
                    cv.line(frm, cofbot, normal, (255, 0, 0), 2)
                    dist_dest = utils.dist(cofbot, S_cnt)
                    _, angle = utils.anglechecker(cofbot, fofbot, S_cnt)
                    # if the bot is on mid
                    if not forwarded and utils.dist(cofbot, mid) < Induct_Dist_Thres:
                        # if the bot turned right and is ready to move fwd

                        #start turning the bot to the right for 0 <= n <= 1
                        print("Turning")
                        control(id, 3, direction=1, pwm=int(Speed_pwm // 1.5))
                        if 0 <= n <= 1:
                            control(id, 2, direction=2)
                            print("Right")
                        elif 2 <= n <= 3:
                            print("Left")
                            control(id, 1, direction=2)
                        print(angle, dist_normal)
                        if abs(angle) < Bot_Angle_Thres and abs(dist_normal) < Induct_Dist_Thres:  # new threshold
                            print("Bot is forwarded")
                            control(id, 3, direction=1, pwm=Speed_pwm)  # forwards the bot
                            forwarded = True

                    # additional logic inside!!!
                    # scope 4 exiter section
                    if dist_dest < Induct_Dist_Thres:
                        isReturn = False
                        forwarded = False
                        pwm_r = Speed_pwm
                        pwm_l = Speed_pwm
                        pwm_b = Speed_pwm
                        print("Bot stops")
                        control(id, 3, direction=0, pwm=0)
                        # after bot stops, selector 'n' points to the next bot
                        print(n)
                        n += 1
                        print("goes to ")
                        print(n)
                # end of vertical return locomotion scope

    cv.aruco.drawDetectedMarkers(frm, markerCorners)
    cv.imshow("Frame", rescaleFrame(frm))

cap.release()
cv.destroyAllWindows()
