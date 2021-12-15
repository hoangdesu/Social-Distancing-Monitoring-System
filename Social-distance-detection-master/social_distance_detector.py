# USAGE
# python social_distance_detector.py --input pedestrians.mp4
# python social_distance_detector.py --input pedestrians.mp4 --output output.avi

# import the necessary packages
from TheLazyCoder import social_distancing_config as config
from TheLazyCoder.detection import detect_people
from scipy.spatial import distance as dist
import numpy as np
import argparse
import imutils
import cv2
import os
import time

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", type=str, default="",
	help="path to (optional) input video file")
ap.add_argument("-o", "--output", type=str, default="",
	help="path to (optional) output video file")
ap.add_argument("-d", "--display", type=int, default=1,
	help="whether or not output frame should be displayed")
ap.add_argument("-v", "--variation", type=str,default="v4",
	help="which kind of YoloV3 variation to be used")
args = vars(ap.parse_args())

# load the COCO class labels our YOLO model was trained on
labelsPath = os.path.sep.join([config.MODEL_PATH, "coco.names"])
LABELS = open(labelsPath).read().strip().split("\n")

if(args["variation"] == "tiny"):
	print("TINY")
	variation_weights = "yolov3-tiny.weights"
	variation_cfg = "yolov3-tiny.cfg"
elif(args["variation"] == "v4"):
	print("v4")
	variation_weights = "yolov4-person.weights"
	variation_cfg = "yolov4-person.cfg"
elif(args["variation"] == "normal"):
	print("v3_normal")
	variation_weights = "yolov3.weights"
	variation_cfg = "yolov3.cfg"


# derive the paths to the YOLO weights and model configuration
weightsPath = os.path.sep.join([config.MODEL_PATH, variation_weights])
configPath = os.path.sep.join([config.MODEL_PATH, variation_cfg])

# load our YOLO object detector trained on COCO dataset (80 classes)
print("[INFO] loading YOLO from disk...")
net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)

# check if we are going to use GPU
if config.USE_GPU:
	# set CUDA as the preferable backend and target
	print("[INFO] setting preferable backend and target to CUDA...")
	net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
	net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

# determine only the *output* layer names that we need from YOLO
# ln = net.getLayerNames()
# ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

ln = net.getUnconnectedOutLayersNames()  

# initialize the video stream and pointer to output video file
print("[INFO] accessing video stream...")
vs = cv2.VideoCapture(0)

# used to record the time when we processed last frame
prev_frame_time = 0
 
# used to record the time at which we processed current frame
new_frame_time = 0

#vs = cv2.VideoCapture(args["input"] if args["input"] else 1)
writer = None

# loop over the frames from the video stream
while True:
	# read the next frame from the file
	(grabbed, frame) = vs.read()

	# if the frame was not grabbed, then we have reached the end
	# of the stream
	if not grabbed:
		break

	# resize the frame and then detect people (and only people) in it
	frame = imutils.resize(frame, width=700)
	results = detect_people(frame, net, ln,
		personIdx=LABELS.index("person"))

	# initialize the set of indexes that violate the minimum social
	# distance
	violate = set()

	#Indicating whether there is a crowd gathered within the frame
	crowd_bool = False

	# ensure there are *at least* two people detections (required in
	# order to compute our pairwise distance maps)
	if len(results) >= 2:
		# extract all centroids from the results and compute the
		# Euclidean distances between all pairs of the centroids
		centroids = np.array([r[2] for r in results])
		D = dist.cdist(centroids, centroids, metric="euclidean")

		# loop over the upper triangular of the distance matrix
		for i in range(0, D.shape[0]):
			for j in range(i + 1, D.shape[1]):
				# check to see if the distance between any two
				# centroid pairs is less than the configured number
				# of pixels
				if D[i, j] < config.MIN_DISTANCE:
					# update our violation set with the indexes of
					# the centroid pairs
					violate.add(i)
					violate.add(j)

	# if len(violate) >= 4:
	# 	crowd_pp = np.array([v[4] for v in results])
	# 	D_crowd = dist.cdist(crowd_pp, crowd_pp, metric="euclidean")
				
	# 	for i in range(0, D_crowd.shape[0]):
	# 		for j in range(i + 1, D_crowd.shape[1]):
	# 			# check to see if the distance between any two
	# 			# centroid pairs is less than the configured number
	# 			# of pixels
	# 			if D_crowd[i, j] < config.MIN_DISTANCE:
	# 				crowd_bool = True

	# loop over the results
	for (i, (prob, bbox, centroid)) in enumerate(results):
		# extract the bounding box and centroid coordinates, then
		# initialize the color of the annotation
		(startX, startY, endX, endY) = bbox
		(cX, cY) = centroid
		color = (0, 255, 0)

		# if the index pair exists within the violation set, then
		# update the color
		if i in violate:
			color = (0, 0, 255)

		# draw (1) a bounding box around the person and (2) the
		# centroid coordinates of the person,
		cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
		cv2.circle(frame, (cX, cY), 5, color, 1)

 	# Calculating the fps

	# time when we finish processing for this frame
	new_frame_time = time.time()
    # fps will be number of frame processed in given time frame
    # since their will be most of time error of 0.001 second
    # we will be subtracting it to get more accurate result
	fps = 1/(new_frame_time-prev_frame_time)
	prev_frame_time = new_frame_time
 
    # converting the fps into integer
	fps = int(fps)
 
    # converting the fps to string so that we can display it on frame
    # by using putText function
	fps = str(fps)
 
    # putting the FPS count on the frame
	cv2.putText(frame, fps, (7, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (100, 255, 0), 3, cv2.LINE_AA)

	# draw the total number of social distancing violations on the
	# output frame
	text = "Social Distancing Violations: {}".format(len(violate))
	cv2.putText(frame, text, (10, frame.shape[0] - 25),
		cv2.FONT_HERSHEY_SIMPLEX, 0.85, (0, 0, 255), 3)

	# Show if there's crowd gather 
	text = "Crowd gathered: {}".format(crowd_bool)
	cv2.putText(frame, text, (10, frame.shape[0] - 50),
		cv2.FONT_HERSHEY_SIMPLEX, 0.85, (0, 0, 255), 3)

	# check to see if the output frame should be displayed to our
	# screen
	if args["display"] > 0:
		# show the output frame
		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF

		# if the `q` key was pressed, break from the loop
		if key == ord("q"):
			break

	# if an output video file path has been supplied and the video
	# writer has not been initialized, do so now
	if args["output"] != "" and writer is None:
		# initialize our video writer
		fourcc = cv2.VideoWriter_fourcc(*"MJPG")
		writer = cv2.VideoWriter(args["output"], fourcc, 25,
			(frame.shape[1], frame.shape[0]), True)

	# if the video writer is not None, write the frame to the output
	# video file
	if writer is not None:
		writer.write(frame)
