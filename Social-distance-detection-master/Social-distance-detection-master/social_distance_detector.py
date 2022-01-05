# USAGE
# python social_distance_detector.py --input pedestrians.mp4
# python social_distance_detector.py --input pedestrians.mp4 --output output.avi

# import the necessary packages
from TheLazyCoder import social_distancing_config as config
from TheLazyCoder.detection import detect_people
from bird_view_functions import compute_perspective_transform,compute_point_perspective_transformation
from scipy.spatial import distance as dist
from Colors import bcolors
import numpy as np
import argparse
import imutils
import cv2
import os
import time
import yaml
import itertools
import math
import threading
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO
from flask import Response, request, Flask

COLOR_RED = (0, 0, 255)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (255, 0, 0)
BIG_CIRCLE = 60
SMALL_CIRCLE = 3

######################################### 
#     TODO: Triet	#
#########################################
# Flask App 1 For Human Detection
app = Flask(__name__)
frame = None
app.config['SECRET_KEY'] = 'dreamchaser'
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
socketio = SocketIO(app, cors_allowed_origins="*")
######################################### 
#     TODO: Triet	#
#########################################

def get_centroids_and_groundpoints(array_boxes_detected, centroids):
	"""
	For every bounding box, compute the centroid and the point located on the bottom center of the box
	@ array_boxes_detected : list containing all our bounding boxes 
	"""
	array_groundpoints = [] # Initialize empty centroid and ground point lists 
	for index,box in enumerate(array_boxes_detected):
		# Draw the bounding box 
		# Get the both important points
		ground_point = get_points_from_box(box, centroids[index])
		array_groundpoints.append(ground_point)
	return array_groundpoints
	# (startX, startY, endX, endY) = box
	# (center_x, center_y) = centroid
	# # Coordiniate on the point at the bottom center of the box
	# center_y_ground = center_y + ((endY - startY)/2)
	# return (center_x,center_y),(center_x,int(center_y_ground))

def get_points_from_box(box, centroid ):
	"""
	Get the center of the bounding and the point "on the ground"
	@ param = box : 2 points representing the bounding box
	@ return = centroid (x1,y1) and ground point (x2,y2)
	"""
	# Center of the box x = (x1+x2)/2 et y = (y1+y2)/2
	(startX, startY, endX, endY) = box
	(center_x, center_y) = centroid
	# Coordiniate on the point at the bottom center of the box
	center_y_ground = center_y + ((endY - startY)/2)
	return (center_x,int(center_y_ground))


def draw_rectangle(corner_points):
	# Draw rectangle box over the delimitation area
	cv2.line(frame, (corner_points[0][0], corner_points[0][1]), (corner_points[1][0], corner_points[1][1]), COLOR_BLUE, thickness=1)
	cv2.line(frame, (corner_points[1][0], corner_points[1][1]), (corner_points[3][0], corner_points[3][1]), COLOR_BLUE, thickness=1)
	cv2.line(frame, (corner_points[0][0], corner_points[0][1]), (corner_points[2][0], corner_points[2][1]), COLOR_BLUE, thickness=1)
	cv2.line(frame, (corner_points[3][0], corner_points[3][1]), (corner_points[2][0], corner_points[2][1]), COLOR_BLUE, thickness=1)

def bfs(graph, node): #function for BFS
	visited = [] # List for visited nodes.
	queue = [] # init a queue
	visited.append(node)
	queue.append(node)

	while queue:          # Creating loop to visit each node
		m = queue.pop(0) 

		for neighbour in graph[m]:
			if neighbour not in visited:
				visited.append(neighbour)
				queue.append(neighbour)

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

#TODO: NAM
######################################### 
# Load the config for the top-down view #
#########################################
print(bcolors.WARNING +"[ Loading config file for the bird view transformation ] "+ bcolors.ENDC)
with open("config_birdview.yml", "r") as ymlfile:
    cfg = yaml.load(ymlfile)
width_og, height_og = 0,0
corner_points = []
for section in cfg:
	corner_points.append(cfg["image_parameters"]["p1"])
	corner_points.append(cfg["image_parameters"]["p2"])
	corner_points.append(cfg["image_parameters"]["p4"])
	corner_points.append(cfg["image_parameters"]["p3"])
	##### NEW
	point_1 = cfg["image_parameters"]["p5"]
	point_2 = cfg["image_parameters"]["p6"]
	##### NEW
	width_og = int(cfg["image_parameters"]["width_og"])
	height_og = int(cfg["image_parameters"]["height_og"])
	img_path = cfg["image_parameters"]["img_path"]
	size_frame = cfg["image_parameters"]["size_frame"]
print(bcolors.OKGREEN +" Done : [ Config file loaded ] ..."+bcolors.ENDC )

print(img_path)
######################################### 
# load the COCO class labels our YOLO model was trained on #
#########################################
labelsPath = os.path.sep.join([config.MODEL_PATH, "coco.names"])
LABELS = open(labelsPath).read().strip().split("\n")
filename = ""
fileWritable = False

if(args["variation"] == "tiny-v3"):
	print("TINY")
	variation_weights = "yolov3-tiny.weights"
	variation_cfg = "yolov3-tiny.cfg"
	filename = "tiny-v3.txt"
elif(args["variation"] == "v4"):
	print("v4-person")
	variation_weights = "yolov4-person.weights"
	variation_cfg = "yolov4-person.cfg"
	filename = "v4-person.txt"
elif(args["variation"] == "normal-v3"):
	print("v3_normal")
	variation_weights = "yolov3.weights"
	variation_cfg = "yolov3.cfg"
	filename = "normal-v3.txt"
elif(args["variation"] == "csp"):
	print("v4_csp")
	variation_weights = "yolov4-csp.weights"
	variation_cfg = "yolov4-csp.cfg"
	filename = "csp.txt"
elif(args["variation"] == "tiny-v4"):
	print("v4_csp")
	variation_weights = "yolov4-tiny.weights"
	variation_cfg = "yolov4-tiny.cfg"
	filename = "v4_csp.txt"
elif(args["variation"] == "v4"):
	print("v4_csp")
	variation_weights = "yolov4.weights"
	variation_cfg = "yolov4.cfg"


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



######################################### 
#     Compute transformation matrix		#
#########################################
# Compute  transformation matrix from the original frame
matrix,imgOutput = compute_perspective_transform(corner_points,width_og,height_og,cv2.imread(img_path))
height,width,_ = imgOutput.shape
blank_image = np.zeros((height,width,3), np.uint8)
height = blank_image.shape[0]
width = blank_image.shape[1] 
dim = (width, height)

d_point_1 = compute_point_perspective_transformation(matrix,point_1)
d_point_2 = compute_point_perspective_transformation(matrix,point_2)
print(d_point_1, d_point_2)
min_dis = int(dist.euclidean(d_point_1, d_point_2))
print('Distance in pixels: '+ str(min_dis))

# initialize the video stream and pointer to output video file
print("[INFO] accessing video stream...")
vs = cv2.VideoCapture(0)
#vs = cv2.VideoCapture("PETS2009.avi")
#vs = cv2.VideoCapture(0)


# used to record the time when we processed last frame
prev_frame_time = 0
 
# used to record the time at which we processed current frame
new_frame_time = 0

#vs = cv2.VideoCapture(args["input"] if args["input"] else 1)
writer = None

crowd_frame_counter = 0

######################################### 
#     FRAME TASKs	#
#########################################
######################################### 
#     TODO: Triet	#
#########################################
def stream():
	global prev_frame_time
	global writer
	global crowd_frame_counter
	# loop over the frames from the video stream
	while True:
		bird_view_img = cv2.resize(blank_image, dim, interpolation = cv2.INTER_AREA)

		# read the next frame from the file
		(grabbed, frame) = vs.read()

		# if the frame was not grabbed, then we have reached the end
		# of the stream
		if not grabbed:
			break
		else:
			# resize the frame and then detect people (and only people) in it
			frame = imutils.resize(frame, width=int(size_frame))

			results = detect_people(frame, net, ln,
				personIdx=LABELS.index("person"))

			d_list = []
			if len(results) > 0:
				centroids = np.array([r[2] for r in results])
				array_boxes_detected = np.array([r[1] for r in results])
				# d_list = []
				# Transform bounding boxes from YOLO to downoids point on the calibrated view
				# for (i, (prob, bbox, centroid)) in enumerate(results):
					# extract the bounding box and centroid coordinates, then
					# initialize the color of the annotation

				# Both of our lists that will contain the centroïds coordonates and the ground points
				array_groundpoints = get_centroids_and_groundpoints(array_boxes_detected, centroids)
				# print(array_groundpoints)
				# Use the transform matrix to get the transformed coordinates
				d_list = compute_point_perspective_transformation(matrix,array_groundpoints)
				# d_list.append(transformed_downoids)

			# initialize the set of indexes that violate the minimum social
			# distance
			distance_violate = set()
			possible_crowd = set()
			crowd = dict()
			#Indicating whether there is a crowd gathered within the frame
			crowd_counter_flag = False
			crowd_bool = False
			
			# ensure there are *at least* two people detections (required in
			# order to compute our pairwise distance maps)
			if len(d_list) >= 2:
				D = dist.cdist(d_list, d_list, metric="euclidean")
				# print(D)
				# loop over the upper triangular of the distance matrix
				for i in range(0, D.shape[0]):
					for j in range(i + 1, D.shape[1]):
						# check to see if the distance between any two
						# centroid pairs is less than the configured number
						# of pixels

						if D[i, j] < min_dis+20:
							# update our violation set with the indexes of
							# the centroid pairs
							l = [i,j]
							possible_crowd.add(tuple(l))
							if D[i, j] < min_dis:
								distance_violate.add(i)
								distance_violate.add(j)


				
			if len(possible_crowd) > 0:
				for i,pair in enumerate(itertools.combinations(possible_crowd, r=2)):
					set_0 = set(pair[0])
					set_1 = set(pair[1])
					inter = set_0.intersection(set_1)
					if (len(inter) > 0):
						difference0_1 = (set_0 - set_1).pop()
						difference1_0 = (set_1 - set_0).pop()
						crowd[inter.pop()] = [difference0_1,difference1_0]
						crowd_frame_counter += 1
					
			
			# # loop over the results
			for (i, (prob, bbox, centroid)) in enumerate(results):
				# extract the bounding box and centroid coordinates, then
				# initialize the color of the annotation
				(startX, startY, endX, endY) = bbox
				(cX, cY) = centroid
				
				# # if the index pair exists within the violation set, then
				# # update the color
				if i in distance_violate:
					color = (0, 0, 255)
				else:
					color = (0, 255, 0)

				# draw (1) a bounding box around the person and (2) the
				# centroid coordinates of the person,
				cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
				cv2.circle(frame, (cX, cY), 5, color, 1)

				point = d_list[i]
				x,y = point
				cv2.circle(bird_view_img, (int(x),int(y)), 5, color, -1)

				
			
			# Traversing the crowd graph to draw the conenction between them 
			if len(crowd) > 0:
				centroids = np.array([r[2] for r in results]) 
				first_node = next(iter(crowd))
				visited = [] # List for visited nodes.
				queue = [] # init a queue
				visited.append(first_node)
				queue.append(first_node)
				while queue:          # Creating loop to visit each node
					m = queue.pop(0) 
					startX, startY = d_list[m]
					startX_frame, startY_frame = centroids[m]
					if m in crowd:
						for neighbour in crowd[m]:
							endX, endY = d_list[neighbour]
							endX_frame, endY_frame = centroids[neighbour]
							line_color = (255, 128, 0)
							cv2.line(bird_view_img,(int(startX),int(startY)), (int(endX),int(endY)), line_color, 2 )
							cv2.line(frame,(int(startX_frame),int(startY_frame)), (int(endX_frame),int(endY_frame)), line_color, 2 )
							if neighbour not in visited:
								visited.append(neighbour)
								queue.append(neighbour)
			else:
				crowd_frame_counter = 0
					
			
			# When the crowd still persist for 20 frame (1 second)
			if crowd_frame_counter > 5:
				crowd_bool = True
				crowd_frame_counter = 0
			

			# time when we finish processing for this frame
			new_frame_time = time.time()
			# fps will be number of frame processed in given time frame
			# since their will be most of time error of 0.001 second
			# we will be subtracting it to get more accurate result
			fps = 1/(new_frame_time-prev_frame_time)
			prev_frame_time = new_frame_time
		
			# converting the fps into integer
			fps = int(fps)
			fps = str(fps)

			if fileWritable is True:
				file = open(filename,"a") 
				file.write(fps)
				file.write("\n")
				file.close()
			# converting the fps to string so that we can display it on frame
			# by using putText function
			
		
			# putting the FPS count on the frame
			cv2.putText(frame, fps, (7, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (100, 255, 0), 3, cv2.LINE_AA)

			# draw the total number of social distancing violations on the
			# output frame
			text = "Social Distancing Violations: {}".format(len(distance_violate))
			cv2.putText(frame, text, (10, frame.shape[0] - 25),
				cv2.FONT_HERSHEY_SIMPLEX, 0.85, (0, 0, 255), 3)

			# Show if there's crowd gather 
			text = "Crowd gathered: {}".format(crowd_bool)
			cv2.putText(frame, text, (10, frame.shape[0] - 50),
				cv2.FONT_HERSHEY_SIMPLEX, 0.85, (0, 0, 255), 3)

		# check to see if the output frame should be displayed to our
		# screen
		if args["display"] > 0:
			# Draw the green rectangle to delimitate the detection zone
			draw_rectangle(corner_points)
			# Show both images	
			cv2.imshow("Bird view", bird_view_img)
			# show the output frame
			cv2.imshow("Frame", frame)

			h,w,c = frame.shape
			h1,w1,c1 = bird_view_img.shape

			if h != h1 or w != w1: # resize right img to left size
				bird_view_img = cv2.resize(bird_view_img,(w,h))
				
			vis = np.concatenate((frame, bird_view_img), axis=1)
			key = cv2.waitKey(1) & 0xFF

			(flag, encodedImage) = cv2.imencode(".jpg", vis)
			yield(b'--vis\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')

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

@app.route("/video_feed")
@cross_origin()
def video_feed():
    # return the response generated along with the specific media
    # type (mime type)
    return Response(stream(),
        mimetype = "multipart/x-mixed-replace; boundary=vis")

if __name__ == '__main__':
	app.run(host="0.0.0.0", port=9099, debug=True, threaded=True, use_reloader=True)
	# video stream service
	t = threading.Thread(target=stream)
	t.daemon = True
	t.start()

######################################### 
#     TODO: Triet	#
#########################################