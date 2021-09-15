import utils
import cv2
from tracker import *
import time

from mqtt_router import control, cred
from arenatrack import obt
from computer import comp


tracker = EuclideanDistTracker()

cap = cv2.VideoCapture(1)

object_detector = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=10)


def change_res(width, height):
    cap.set(3,width)
    cap.set(4,height)

#change_res(1920,1080)
dist=[]
start=True
mid=False
drop=False
Return= False
End=False
straight=True
id=0
'''
while 1:
    if cred.bots:
        id= cred.bots[0]
        print('id:',id)
        break
'''
pl=obt()
print('pppppllllll::',pl)
while True:
    
    ret, frame = cap.read()
    
    #TODO: Check the height and width of your frame and put it in line 26
    height, width, _ = frame.shape
    #print(height, width)
    #break

    #time.sleep()

    #print("Manish",height,width)
    #time.delay(5)
    
    roi = frame[:,350: 550]

    
    '''
    mask = object_detector.apply(roi)
    _, mask = cv2.threshold(mask, 200, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    '''
    detections = []
    '''
    for cnt in contours:
        
        
        area = cv2.contourArea(cnt)
        print(area) #TODO: check the area of your bot and accordingly set the if condition
        time.sleep(0.951)
        
        
        if 50< area < 100:
            
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(roi,(x,y),(x+w,y+h),(230,45,189)) 
    '''  
    x,y,w,h=pl[0][0],pl[0][1],pl[0][2],pl[0][3]
    
    detections.append([x+400, y+200, w, h])

    boxes_ids = tracker.update(detections)
    
    for box_id in boxes_ids:
        x, y, w, h, id = box_id
        
        
        cv2.putText(roi, str(id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 5)
        cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 3)
        cofbot=((x+w//2),(y+h//2))
        fofbot=(((x+w)-x)//2,y)
        cv2.circle(roi,cofbot,3,(0,0,255),-1)
        #cv2.putText(frame, str(time.time()), (x, y - 40), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 5)
        
        if not Return:

            endpnt=(15,200) # TODO: #d1 point
        else:
            endpnt=(150,220) # TODO: #s1 point 

        cv2.circle(roi,endpnt,7,(0,0,255),-1)
        

        xy=utils.std(cofbot,endpnt)
        cv2.circle(roi,xy,5,(0,0,255),-1)
        cv2.line(roi,cofbot,xy,(122,122,210),7)
        cv2.line(roi,xy,endpnt,(122,122,10),7)
        cv2.arrowedLine(roi,cofbot,fofbot,(100,100,100),3, cv2.LINE_AA)
        straight,theta=utils.anglechecker(cofbot,fofbot,endpnt)
        cv2.putText(roi, str(theta), (cofbot), cv2.FONT_HERSHEY_PLAIN, 2, (255, 20, 100), 5)
        if not Return:
            dist1=utils.dist(cofbot,xy)
            dist2=utils.dist(xy,endpnt)
        else:
            dist2r=utils.dist(cofbot,xy)
            dist1r=utils.dist(xy,endpnt)


        
        # 0-> stop
        # 1 -> forward
        # 2 -> right
        # 3-> left
        '''
        if not mid:
            mid=utils.checker(id,dist,dist1)
        #print(mid)
        if start and not mid:
            continue
        else:
            # start=False
            #print(mid)
            straight,theta=utils.anglechecker(cofbot,fofbot,endpnt)
            cv2.line(roi,cofbot,fofbot,(0,0,0),7)
            cv2.line(roi,cofbot,endpnt,(0,0,0),7)
            #cv2.putText(roi, str(theta), (cofbot), cv2.FONT_HERSHEY_PLAIN, 2, (255, 20, 100), 5)
            print("huurrah!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print(theta)
            print("Now chwck id and rotate accordingly!............")
            if not straight:
                if (id<2):
                    control(id, 2, direction=1)
                    control(id,3,direction=0)
                    print("turning right 90deg")
                    
                else:
                    control(id,1,direction=1)
                    control(id,3,direction=0)
                    print("turning left 90deg") 
            print(dist,dist2)
            drop=utils.checker(dist,dist2)
            print(dist,dist2,"d2")
            #print(drop)
            if mid and not drop:
                continue
            else:
                #TODO: Throw package command
                control(id,3,direction=0)
                if Return:
                    start=False
                if drop:
                    Return=True
        if Return :
            print("returning!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print("rotating!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!----------------------------")
            if (id<2):
                comp(2)
                comp(0)
                print("turning right 90deg")
                
            else:
                comp(3)
                comp(0)
                print("turning left 90deg")
            if (id<2):
                comp(2)
                comp(0)
                print("turning right 90deg")
                
            else:
                comp(3)
                comp(0)
                print("turning left 90deg")

            mid=False
            drop=False
        if not start and Return and drop:
            print("DONNNEEEEEE-------------------------------------------------------------------.........")
            id+=1
            start=True
            mid=False
            drop=False
            Return= False
            End=False
            straight=True
    '''
    
    if ret:
        cv2.imshow("Frame", frame)
        cv2.imshow("roi", roi)
        #cv2.imshow("mask", mask)
    time.sleep(0.095)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break
    

cap.release()
cv2.destroyAllWindows()