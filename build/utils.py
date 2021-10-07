import math
from math import *

from cv2 import PCACompute2


def dist(a, b):
    # two tuples/ coordinates
    return int(math.dist(a, b))


def xyd(a, b):
    x1, y1 = a[0], a[1]
    x2, y2 = b[0], b[1]
    x = abs(x2 - x1)
    y = abs(y2 - y1)
    return (x, y)


def std_v(a, b):
    return (a[0], b[1])


def std_h(a, b):
    return (b[0], a[1])


def pid(cofbot, dest):
    cob = cofbot[0] - dest[0]
    print(cob)
    if cob > 10:
        return 2
    elif cob < -10:
        return 1
    else:
        return 3

def anglechecker(centre, pt1, edge):
    (x1, y1) = pt1
    (x2, y2) = edge
    (x, y) = centre
    if x1 != x:
        m1 = (y1 - y)//(x1 - x)
    else:
        m1 = None # implies slope is 90 deg
    if x2 != x:
        m2 = (y2 - y)//(x2 - x)
    else:
        m2 = None
    angle: int
    # if m1 is None or m2 is None:
    if m1 is None and m2 is None:
        angle = 0 # lines are parallel
    elif m1 is None:
        rad = atan(m2)
        angle = round(90 - degrees(rad))
    elif m2 is None:
        rad = atan(m1)
        angle = round(90 - degrees(rad))
    else:
        if m1*m2 == -1:
            angle = 90
        else:
            rad = atan((m2 - m1) / (1 + (m1 * m2)))
            angle = round(degrees(rad))
    if abs(angle) > 90:
        angle = 180 - angle
    return False, angle

 
# def anglechecker(centre, pt1, edge):
#     (x, y) = centre
#     (x1, y1) = pt1
#     x2, y2 = edge[0], edge[1]
#     if x == x1:
#         m1 = 1
#     else:
#         m1 = (y - y1) / (x - x1)
#     if x == x2:
#         m2 = 1
#     else:
#         m2 = (y - y2) / (x - x2)
#     # print('m1:',m1,'m2:', m2)
#     # if (m1 == 1 and abs(m2) == 0) or (m2 == 1 and abs(m1) == 0):
#     if m1*m2 == -1:
#         theta = 90
#     else:
#         rad = atan((m2 - m1) / (1 + (m1 * m2)))
#         theta = round(degrees(rad))

#     # print(theta)
#     # if theta<0:
#     #     theta=-(theta)
#     if theta <= 5:
#         return True, theta
#     return False, theta


def checker(dist, dist1):
    # print(dist,dist1)
    val = False
    if dist:
        if (dist1 <= 50):
            # print(dist1)
            dist1 = 0
            dist.pop()
            print("stop")
            # dist1=dist2
            val = True

        elif (dist1 < dist[-1]):
            dist.pop()
            dist.append(dist1)
            print("forward")

    else:
        # if dist1:
        dist.append(dist1)
        # print(dist1)
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


def find_coordinates(markerCorners, c):
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

def pwm_deductor(dist, var_dist):
    if (var_dist - dist) in range(0, 25):
        return 60
    elif (var_dist - dist) in range(40, 150):
        return 30
    elif (var_dist - dist) in range(150, 300):
        return 7
    else:
        return 2