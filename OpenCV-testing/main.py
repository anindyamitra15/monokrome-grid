import utils
import cv2
from tracker import *
import time
import numpy as np
import sys

from mqtt_router import *
#from arenatrack import obt
#from computer import comp


#tracker = EuclideanDistTracker()

cap = cv2.VideoCapture(0)

#object_detector = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=10)


def change_res(width, height):
    cap.set(3,width)
    cap.set(4,height)

change_res(1920,1080)
dist=[]
start=True
turnj=False
mid=False
midr=False
drop=False
dropr=False
Return= False
End=False
straight=True

'''
while 1:
    if cred.bots:
        id= cred.bots[0]
        print('id:',id)
        break
'''
# pl=obt()
# print('pppppllllll::',pl)
flag=True
while True:
    ret, frame = cap.read()
    # roi = frame[:, 350: 550]  #to be used later

    cnv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    if ret is False:
        sys.exit()
    else:
        # all bots have same colour, my plan is to hard code mqtt to gib instructions
        # to a bot for a definite amount of time and then switch to the next bot
        # and use an exit sequence to trigger exit after the above procedure happens 4 times
        # hsv space of bot colour
        lower_hue = 0
        lower_saturation = 140
        lower_value = 165
        upper_hue = 179
        upper_saturation = 255
        upper_value = 255


        lower, upper = np.array([lower_hue, lower_saturation, lower_value]), np.array([upper_hue, upper_saturation, upper_value])

        #cv2.imshow("hsv", cnv_frame)
        mask = cv2.inRange(cnv_frame, lower, upper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        img = cv2.bitwise_and(frame, frame, mask=mask)

        cv2.imshow('maskedddd', mask)

        # problems arising with contour detection, to be solved
        # will use mask.copy() at final stage as img gets modified in find contours func

        contours, h = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #cv2.imshow("After contour detection", mask)

        cnts = sorted(contours, key=cv2.contourArea, reverse=True)[:1]  # stores first 10 largest contour points
        #time.sleep(5)
        c = max(cnts, key=cv2.contourArea)
        #print(cnts[0])
        # for cnt in contours:
        #     #print('haha')
        x, y, w, h = cv2.boundingRect(c)
        #roi = frame[x:x+w,y:y+h]
        #cv2.imshow("Roi",roi)
        #
        #     break
        if w > 10:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.rectangle(frame, (int(x), int(y)), (int(x + w), int(y + h)),
                          (0, 255, 255), 2)
            cv2.circle(frame, (int(x + w / 2), int(y + h / 2)), 2, (0, 0, 255), -1)
            text = "({},{})".format(int(x + w / 2), int(y + h / 2))
            #cv2.putText(frame, text, (int(x), int(y - 10)), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)
            #print(text)
        cofbot = ((x + w // 2), (y + h // 2))
        
        if flag:
            s1=cofbot
            flag=False
        if start:
            fofbot = (x + w // 2, y)
        elif End:
            fofbot=(x+w//2,y+h)
        elif turnj:
            fofbot=(x+w,y+h//2)
        elif Return:
            fofbot=(x,y+h//2)
              
        #cv2.circle(frame, cofbot, 3, (0, 0, 255), -1)


        if not Return:

            endpnt=(1400,325) # TODO: #d1 point
        else:
            endpnt=s1 # TODO: #s1 point 

        cv2.circle(frame,endpnt,7,(0,0,255),-1)
        roi=frame
        if not Return:
            xy=utils.std(cofbot,endpnt)
        else:
            xy=utils.std(endpnt,cofbot)
        cv2.circle(roi,xy,5,(0,0,255),-1)
        cv2.line(roi,cofbot,xy,(122,122,210),7)
        cv2.line(roi,xy,endpnt,(122,122,10),7)
        cv2.arrowedLine(roi,cofbot,fofbot,(100,100,100),3, cv2.LINE_AA)
        #straight,theta=utils.anglechecker(cofbot,fofbot,endpnt)
        #cv2.putText(roi, str(theta), (cofbot), cv2.FONT_HERSHEY_PLAIN, 2, (255, 20, 100), 5)
        cv2.imshow("Frame", frame)
        if not Return:
            dist1=utils.dist(cofbot,xy)
            dist2=utils.dist(xy,endpnt)
        else:
            dist1=utils.dist(cofbot,xy)
            dist2=utils.dist(xy,endpnt)

        #control(7892874, 1, direction=1, pwm=250)

        #control(7892874, 3, direction=0)
        # 0-> stop
        # 1 -> forward
        # 2 -> right
        # 3-> left
        idl = [7892874,7893554]
        id=idl[1]
        if start :
        
            mid=utils.checker(dist,dist1)
    
            if(mid):
                print("stop")
                control(id, 3, direction=0, pwm=0)
                # control(id, 1, direction=0, pwm=0)
                # control(id, 2, direction=0, pwm=0)


            else:
                print("forward")
                #control(id, 3, direction=1, pwm=200)
                control(id, 1, direction=1, pwm=200)
                control(id, 2, direction=1, pwm=200)


            print('kgklhlvijgl', start,mid)



        
        if mid:
            print("now take aaaaaaknvlnrc;eml;emv;l")

            start=False
            #print(mid)
            straight,theta=utils.anglechecker(cofbot,fofbot,endpnt)
            cv2.line(roi,cofbot,fofbot,(0,0,0),7)
            cv2.line(roi,cofbot,endpnt,(0,0,0),7)
            cv2.putText(roi, str(theta), (cofbot), cv2.FONT_HERSHEY_PLAIN, 2, (255, 20, 100), 5)
            print("huurrah!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print(theta)
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
                straight,theta=utils.anglechecker(cofbot,fofbot,endpnt)
                cv2.line(roi,cofbot,fofbot,(0,0,0),7)
                cv2.line(roi,cofbot,endpnt,(0,0,0),7)
                cv2.putText(roi, str(theta), (cofbot), cv2.FONT_HERSHEY_PLAIN, 2, (255, 20, 100), 5)
                print("huurrah!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print(theta)
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
            id+=1
            '''
            start=True
            mid=False
            drop=False
            Return= False
            End=False
            straight=True
            '''

    if ret:
        cv2.imshow("Frame", frame)
        #cv2.imshow("roi", roi)
        #cv2.imshow("mask", mask)
    #time.sleep(0.05)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break
    

cap.release()
cv2.destroyAllWindows()
