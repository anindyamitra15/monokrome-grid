from math import *

#from computer import comp
from mqtt_router import control

def dist(a,b):
    #two tuples/ coordinates
    return sqrt(((b[0]-a[0])**2)+((b[1]-a[1])**2))

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


def pid(cofbot,dest):
    cob=cofbot[0]-dest[0]
    print(cob)
    if cob > 10:
        return 2
    elif cob< -10:
        return 1
    else:
        return 3


def anglechecker(centre,pt1,edge):
    x,y=centre[0],centre[1]
    x1,y1=pt1[0],pt1[1]
    x2,y2=edge[0],edge[1]
    if (x==x1):
        m1=1
    else:
        m1=(y-y1)/(x-x1)
    if (x==x2):
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
    return False, theta

def checker(dist,dist1):
    #print(dist,dist1)
    val=False
    if dist:
        if(dist1<=50):
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

def mid_pt(a, b):
    return (int((a[0] + b[0]) // 2), int((a[1] + b[1]) // 2))

'''
utilities for ArUco Marker Position calculations
returns the list containing 3 tuples
1.Center coordinates
2. Top Left Corner coodinates
3. Bottom Right Corner coordinates
'''
def find_coordinates (markerCorners, c):
    center = (
        ((int(markerCorners[c][0][0][0]) + int(markerCorners[c][0][2][0])) // 2),
        ((int(markerCorners[c][0][0][1]) + int(markerCorners[c][0][2][1])) // 2)
        )
    left_top_corner = (
                int(markerCorners[c][0][0][0]),
                int(markerCorners[c][0][0][1])
                )
    right_bottom_corner = (
                int(markerCorners[c][0][2][0]),
                int(markerCorners[c][0][2][1])
                )
    return [center, left_top_corner, right_bottom_corner]
