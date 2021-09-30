from math import *

#from computer import comp
from mqtt_router import control

def dist(a,b):
    #two tuples/ coordinates
    x1,y1=a[0],a[1]
    x2,y2=b[0],b[1]
    val=(((x2-x1)**2)+((y2-y1)**2))
    return sqrt(val)

def xyd(a,b):
    x1,y1=a[0],a[1]
    x2,y2=b[0],b[1]
    x=abs(x2-x1)
    y=abs(y2-y1)
    return (x,y)

def std(a,b):
    x1,y1=a[0],a[1]
    x2,y2=b[0],b[1]
    x=x1
    y=y2
    return (x,y)
def frontofbot():
    pass
def pid(cofbot,dest):
    cob=cofbot[0]-dest[0]
    if cob>5:
        return 1
    elif cob<-10:
        return 2


def anglechecker(centre,pt1,edge):
    val=False
    x,y=centre[0],centre[1]
    x1,y1=pt1[0],pt1[1]
    x2,y2=edge[0],edge[1]
    if (x-x1==0):
        m1=1
    else:
        m1=(y-y1)/(x-x1)
    if (x-x2==0):
        m2=1
    else:
        m2=(y-y2)/(x-x2)
    #print('m1:',m1,'m2:', m2)
    if (m1==1 and abs(m2)==0) or (m2==1 and abs(m1)==0):
        theta=90
    else:
        rad=atan((m2-m1)/(1+(m1*m2)))
        
        theta=round(degrees(rad))

    #print(theta)
    if theta<0:
        theta=-(theta)
    if theta<=5:
        return True, theta
    return val, theta

def checker(dist,dist1):
    #print(dist,dist1)
    val=False
    if dist:
        
        if(dist1<=35):
            #print(dist1)
            dist1=0
            dist.pop()
            print("stop")
            
            # dist1=dist2
                
            val = True
            
        elif(dist1<dist[-1]):
            dist.pop()
            dist.append(dist1)
            print("forward")
           
    else:
        #if dist1:
        dist.append(dist1)
        #print(dist1)
    #     # else:
    #     #     dist.append(dist2)
    #     #     print(dist2)

    
    return val



    


