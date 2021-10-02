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

def rescaleFrame(frame, scale=1):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width, height)
    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

# Dictionary to store the ids and coordinates
Point = dict()
# Arena confirmation Loop
# Loop 1
while True:
    ret, frm = cap.read()

    w = cv.waitKey(frame_timing) & 0xff

    if w == ord('q'):
        cap.release()
        cv.destroyAllWindows()
        on_exit()
        sys.exit()

    # Detect the markers in the image
    markerCorners, markerIds, rejectedCandidates = cv.aruco.detectMarkers(
        frm, dictionary, parameters=parameters)
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
    cv.imshow("Frame", rescaleFrame(frm))

print(Location) # GGGGGGGGGGGGGGGGGGGGGGGGGGGGG
# flags initialisation
S1 = Point[Inducts.get_id("S1")]
S2 = Point[Inducts.get_id("S2")]
S3 = Point[Inducts.get_id("S3")]
S4 = Point[Inducts.get_id("S4")]

dist=[]
start=[True]*4
turnj=[False]*4
mid=[False]*4
midr=[False]*4
drop=[False]*4
dropr=[False]*4
Return=[False]*4
End=[False]*4
straight=[True]*4

print("Code Starts")
# while loop
sys.exit()
n = 0
while True:
    ret, frame= cap.read()

    if cv.waitKey(1) & 0xff == ord('q'):
        break


    #algo

    #i want cofbot, xy and endpnt
    cofbot=(0,0)
    xy=(0,0)
    endpnt=(0,0)

    if not Return:
        dist1=utils.dist(cofbot,xy)
        dist2=utils.dist(xy,endpnt)
    else:
        dist1=utils.dist(cofbot,xy)
        dist2=utils.dist(xy,endpnt)
    if start :

        mid[n]=utils.checker(dist,dist1)

        if(mid[n]):
            print("stop")
            control(id, 3, direction=0, pwm=0)
            # control(id, 1, direction=0, pwm=0)
            # control(id, 2, direction=0, pwm=0)


        else:
            print("forward")
            #control(id, 3, direction=1, pwm=200)
            val=utils.pid(cofbot,xy)
            if val==2:
                control(id, 1, direction=1, pwm=279)
                control(id, 2, direction=1, pwm=100)
                print('lefffttttttt ppppiiiddddddddddddddd')
            elif val==1:
                control(id, 2, direction=1, pwm=279)
                control(id, 1, direction=1, pwm=100)
                print('righttttttttttttttttttttt ppppiiiddddddddddddddd')
            control(id, 1, direction=1, pwm=279)
            control(id, 2, direction=1, pwm=290)



        print('kgklhlvijgl', start,mid)




    if mid:
        print("now take aaaaaaknvlnrc;eml;emv;l")

        start=False
        #print(mid)
        #straight,theta=utils.anglechecker(cofbot,fofbot,endpnt)
        # cv.line(roi,cofbot,fofbot,(0,0,0),7)
        # cv.line(roi,cofbot,endpnt,(0,0,0),7)
        # cv.putText(roi, str(theta), (cofbot), cv.FONT_HERSHEY_PLAIN, 2, (255, 20, 100), 5)
        print("huurrah!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        #print(theta)
        print("Now chwck id and rotate accordingly!............")
        #control(id, 3, direction=0,pwm=0)
        if not Return:
            i=10
            while i:
                i-=1
                control(id, 1, direction=1,pwm=500)
                control(id, 2, direction=2,pwm=500)
            mid=False
        turnj=True

        '''
        if not straight:
            if (id==7892874):
                control(id, 2, direction=1,pwm=300)
                control(id,3,direction=0,pwm=0)
                print("turning left 90deg",id )
                #qtime.sleep(2)
                straight = True

            else:
                control(id,1,direction=1)
                control(id,3,direction=0)
                print("turningright 90deg",id )
        else:
            control(id,3,direction=0,pwm=0)
            turnj=True
        '''
    if turnj:
        if not Return:
            # mid=False
            print(dist,dist2)
            drop=utils.checker(dist,dist2)
            print(dist,dist2,"d2")
            print(drop) #TODO: Throw package command
            if(drop):
                print("stop")
                #control(id, 3, direction=0, pwm=0)
                control(id, 1, direction=0, pwm=0)
                control(id, 2, direction=0, pwm=0)


            else:
                print("forward")
                #control(id, 3, direction=1, pwm=pwm)
                control(id, 1, direction=1, pwm=300)
                control(id, 2, direction=1, pwm=300)
        if Return:
            End=True

            drop=utils.checker(dist,dist2)
            if(drop):
                #drop=False
                Return = False
                dropr=True
                print("stop")
                #control(id, 3, direction=0, pwm=0)
                control(id, 1, direction=0, pwm=0)
                control(id, 2, direction=0, pwm=0)


            else:
                print("forward")
                #control(id, 3, direction=1, pwm=pwm)
                control(id, 1, direction=1, pwm=250)
                control(id, 2, direction=1, pwm=250)
            # drop = False
        if drop:
            print('gooooiinnnggg  tttoooo  dddrroopppp',turnj,drop)



    if drop :

        turnj=False
        control(id, 2, direction=0,pwm=0)
        control(id, 1, direction=0,pwm=0)
        if not dropr:
            control(id,0,logic=1)



        if drop:

            Return=True
        drop=False





        # print("returning!")
        # print("rotating!----------------------------")
        # if (id<2):
        #     control(12345678, 1, direction=2, pwm='200')  #calibrate pwm
        #     control(12345678, 2, direction='0', pwm='0')   #calibrate pwm if req
        #     control(12345678, 3, direction='0', pwm='0')
        #     print("turning right 90deg")

        # else:
        #     control(12345678, 2, direction='1', pwm='200')  #calibrate pwm
        #     control(12345678, 1, direction='0', pwm='0')   #calibrate pwm if req
        #     control(12345678, 3, direction='0', pwm='0')
        #     print("turning left 90deg")
        '''
        if (id<2):
            comp(2)
            comp(0)
            print("turning right 90deg")

        else:
            comp(3)
            comp(0)
            print("turning left 90deg")
        '''

    if Return and not End:
        dropr=True
        midr=utils.checker(dist,dist1)

        if midr and not turnj:
            print("stop")
            control(id, 1, direction=0, pwm=0)
            control(id, 2, direction=0, pwm=0)
            print("now take aaaaaaknvlnrc;eml;emv;l")

            #print(mid)
            # straight,theta=utils.anglechecker(cofbot,fofbot,endpnt)
            # cv.line(roi,cofbot,fofbot,(0,0,0),7)
            # cv.line(roi,cofbot,endpnt,(0,0,0),7)
            # cv.putText(roi, str(theta), (cofbot), cv.FONT_HERSHEY_PLAIN, 2, (255, 20, 100), 5)
            print("huurrah!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            #print(theta)
            print("Now chwck id and rotate accordingly!............")
            i=12
            while i:
                i-=1
                control(id, 1, direction=1,pwm=550)
                control(id, 2, direction=2,pwm=550)
            midr=False
            #control(id, 3, direction=0,pwm=0)
            #time.sleep(1.095)
            # control(id, 1, direction=0,pwm=0)
            # control(id, 2, direction=0,pwm=0)
            turnj=True #TODO: DELETE



        else:
            print("reverse")
            control(id, 3, direction=2, pwm=300)
            # control(id, 1, direction=2, pwm=300)
            # control(id, 2, direction=2, pwm=300)

        '''
        print('kgklhlvijgl',Return,mid)

        # mid=False
        # drop=False
        print("returning")
    '''
    if End and utils.checker(dist,dist2):
        print("DONNNEEEEEE-------------------------------------------------------------------.........")
        control(id, 3, direction=0,pwm=0)
        # control(id, 1, direction=0,pwm=0)
        # control(id, 2, direction=0,pwm=0)
        n+=1
cap.release()
cv.destroyAllWindows()
