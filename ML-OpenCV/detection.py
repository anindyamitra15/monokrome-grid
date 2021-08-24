from imutils import contours
from skimage import measure
import numpy as np
import imutils
import cv2

def detect(frame, mask, lower, upper):
	# It converts the BGR color space of image to HSV color space
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	# Apply mask to image
	hsv = cv2.bitwise_and(hsv, hsv, mask=mask)  #syntax cv2.bitwise_and(img_array_1, img_array_2, mask) much like intersection in Venn Diagrams

	# Preparing the mask to overlay
	thresh = cv2.inRange(hsv, lower, upper)  #inRange function is thresholding the HSV image for a range of color within the boundaries (lower,upper)
	#thresh is now an image in HSV format converted from BGR frame captured, only its intersection with mask.png taken and the taken part is thresholded within the range (lower,upper)

	# Perform a series of erosions and dilations to remove any small blobs of noise from the thresholded image
	#all operations are done on the previously configured "thresh" image
	thresh = cv2.erode(thresh, None, iterations=1)   #Syntax: cv2.erode(image, kernel = a structure according to which the erosion is governed(None taken), iterations = number of times the image is to be eroded)
	thresh = cv2.dilate(thresh, None, iterations=1)  #Syntax: cv2.dilate(image, kernel = a structure according to which the erosion is governed(None taken) ,iterations = number of times the image is to be eroded)
	# cv2.erode() erodes away the features of the image "thresh" alongwith boundaries and cv2.dilate() accentuates the remaining lines
	#print(hsv, thresh) #print statement to test output until now

	# Set up the detector with custom parameters
	#In openCV all shapes are known as Blobs
	#OpenCv has a built in function known as SimpleBlobDetector which detects shapes within captured frames(images)
	#Since SimpleBlobDetector has multiple properties, it is taken within a class named params
	#filterByArea fliters the blobs by the area encompassed by them so that small points in a frame having the same shape is not detected
	#fliterByCircularity fliters the blobs based on Circularity property
	#Circularity of a shape = (4 * pi * Area of that shape) / (perimeter of that shape)^2. Max circularity is 1 (a complete circle)
	#filterByColour filters the blob based on it values in HSV space
	#fliterByConvexity filters the blob based on its concave or convex shape, also concavity destroys the circularity in a image
	#filterByInertia filters the blob based on its shape and distribution of mass, much like moment of inertia...it is given as a ratio where ratio is in the range of (0,1)...nearer to 0 signifies a straight line and nearer to 1 signifies a circle
	params = cv2.SimpleBlobDetector_Params()
	params.filterByArea = True
	params.minArea = 30
	params.maxArea = 1000
	params.filterByCircularity = False
	params.filterByColor = False
	params.filterByConvexity = False
	params.filterByInertia = False

	#dectector which will detect blobs based of the earlier specified parameters
	detector = cv2.SimpleBlobDetector_create(params)

	# Detect blobs and save keypoints as np array
	kps = detector.detect(thresh)

	#for debugging purposes
	#number_of_total_blobs = len(kps)
	#print(number_of_total_blobs)
	#keypoints in the image/frame are returned to use as function inputs for utilities.py function. 
	pts = [np.array([kp.pt[0], kp.pt[1]]).astype(int) for kp in kps]

	return pts
