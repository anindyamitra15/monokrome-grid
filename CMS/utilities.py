from itertools import combinations
import numpy as np
import cv2


class Edge:
    def __init__(self, a, b):  # self be the NxN matrix
        self.a = a
        self.b = b
        self.length = np.linalg.norm(a - b)
        # i guess this is giving out the magnitude of the path of the bot to the final position
        # norm of a vector being simply its magnitude i.e sqrt(a^2+b^2)
        # norm of a matrix is the eigenvalue of its matrix i.e the eigenvalue is the factor by which it is stretched

    def __lt__(self, other):  # __lt__(self, other) is a special function for operator overloading, used for overloading < and = operators into class Edge
        return self.length < other.length  # returns a Boolean value (either True or False), used to compare 2 classes of different elements based on length property


def angle_btwn(a, b):  # angle between vectors a and b
    a = a / np.linalg.norm(a)
    b = b / np.linalg.norm(b)
    n = np.cross(a, b)

    # always returns +ve angle value
    if n > 0:  # finding out the quadrant of the angle and changing cos inverse accordingly
        return np.arccos(np.dot(a, b))  # the angles dot returning the a.b/|a||b|
    else:
        return -np.arccos(np.dot(a, b))


# angle btwn fnc is used for finding the angle for the bot to turn in the magnitude of direction

def triangulate(pts):  # triangulating procedure
    #code works just like this code snippet
    """"
from itertools import combinations
import numpy


class Edge:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.length = self.a + self.b

    def __lt__(self, other):
        return self.length < other.length

new_list = list()
new_list_2 = list()
tester = numpy.zeros(2)
tester_class_inst = Edge(2, 6)
for (a, b) in list(combinations([2, 4, 5, 6], 2)):
    z = Edge(a, b)
    new_list.append(z)
new_list.sort()
for i in range(3):
    new_list_2.append(new_list[i].a)
    new_list_2.append(new_list[i].b)
for p in new_list_2:
    if not p == 2 and not p == 6:  # same as np.array_equal(p, diag.a)
        tester = p
print(tester)
print(new_list_2)
z = numpy.radians(60)
val_1, val_2 = numpy.cos(z), numpy.sin(z)
print(val_1, val_2)
R = numpy.array(((val_1, -val_2), (val_2, val_1)))
print(R)
var_new = R.dot(tester - 2)
print(var_new)
    """
    edges = [Edge(a, b) for (a, b) in list(combinations(pts, 2))]  # this line creates a list of class Edge from a list having ptsC2(nCr) values
    edges.sort()  # since individual classes cannot be compared, they have use __lt__ function to enable class comparison and hence edges.sort() sorts the edges list in ascending order

    diag = edges[2]  # hard coded....always taking the 3rd smallest Class Edge...will be a Class that is stored in the list..eg. Edge(2,3), then diag.a = 2 and diag.b = 3

    cnrs = []
    for i in range(3):   #this loop take the a and b values of the first three Edge classes and appends them serially to the list cnrs
        cnrs.append(edges[i].a)  # ADDS ELEMENT TO ARRAY
        cnrs.append(edges[i].b)  #cnrs variable will be like [2, 4, 2, 5, 2, 6]....just like a normal list

    pos = (diag.a + diag.b) / 2  #hard coded, just dividing the sum of elements in the 3rd smallest class by 2 to find the mid-point between two extremities, a single value variable only
    top_left = np.zeros(2)  #[0, 0] is stored in top_left variable, not sure why this is used

    for p in cnrs:
        if not np.array_equal(p, diag.a) and not np.array_equal(p, diag.b):  #if not the values are the diagonal points, then they are taken in top_left var
            top_left = p    #only a single value is stored

    theta = np.radians(45)
    c, s = np.cos(theta), np.sin(theta)
    R = np.array(((c, -s), (s, c)))  #R is a 2D array with elements [ [c, -s] , [s, c] ]

    dirn = R.dot(top_left - pos)  #most probably the dot product of vector R with a scalar (top_left - pos)

    return [pos.astype(int), dirn.astype(int)]  #returns a list having elements [pos, dirn], dirn is a 2D array.,


def navigate(pos, dirn, vtms):  # dirn is 2D array
    rts = [Edge(pos, vtm) for vtm in vtms] #Class List
    rts.sort()

    rt = rts[0]

    if rt.length == 0:
        angle = 0
    else:
        angle = angle_btwn(dirn, (rt.b - rt.a)) #Calling function angle_btwn()

    return [rts, angle, int(rt.length)]


def draw_vtm(frame, vtms): 
    for vtm in vtms:
        cv2.circle(frame, tuple(vtm), 10, (0, 0, 255), 1) #cv2.circle(img, center, radius, color[, thickness[, lineType[, shift]]]) -> img
        cv2.putText(frame, "({},{})".format(vtm[0], vtm[1]), tuple(vtm - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                #cv2.putText: (img, text, org, fontFace, fontScale, color, thickness=..., lineType=..., bottomLeftOrigin=...) -> Any

def draw_pts(frame, pts): 
    for pt in pts:
        cv2.drawMarker(frame, tuple(pt), (0, 255, 0), cv2.MARKER_TILTED_CROSS, 10, 1, 8) #cv2.drawMarker: (img, position, color, markerType=..., markerSize=..., thickness=..., line_type=...) -> Any
        cv2.putText(frame, "({},{})".format(pt[0], pt[1]), tuple(pt - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)


def draw_bot(frame, pos, dirn):
    cv2.line(frame, tuple(pos), tuple(pos + dirn), (0, 0, 255), 1) #cv2.line: (img, pt1, pt2, color, thickness=..., lineType=..., shift=...) -> Any


def draw_rts(frame, pos, rts, angle, dist):
    for (i, rt) in enumerate(rts): #The enumerate object yields pairs containing a count (from start, which defaults to zero) and a value yielded by the iterable argument.
        if i == 0:
            cv2.line(frame, tuple(rt.a), tuple(rt.b), (0, 255, 0), 1)
        if i != 0:
            cv2.line(frame, tuple(rt.a), tuple(rt.b), (0, 0, 255), 1)


def display_msg(frame, msg, color):
    cv2.putText(frame, msg, (10, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)


def remove_vtm(vtms, rt):
    for (i, vtm) in enumerate(vtms):
        if np.array_equal(vtm, rt.b):
            vtms.pop(i) # Poping i'th element of vtms
