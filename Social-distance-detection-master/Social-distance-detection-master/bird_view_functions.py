import numpy as np
import cv2

#TODO: NAM
def compute_perspective_transform(corner_points,width,height,image):
	""" Compute the transformation matrix
    @ corner_points : 4 corner points selected from the image
    @ height, width : size of the image
    """
	# Create an array out of the 4 corner points
	corner_points_array = np.float32(corner_points)
	# Create an array with the parameters (the dimensions) required to build the matrix
	img_params = np.float32([[0,0],[width,0],[0,height],[width,height]])
	# Compute and return the transformation matrix
	matrix = cv2.getPerspectiveTransform(corner_points_array,img_params) 
	img_transformed = cv2.warpPerspective(image,matrix,(width,height))
	return matrix,img_transformed

def compute_point_perspective_transformation(matrix,list_downoids):

	# Compute the new coordinates of our points
	# print("Downoids list")
	# print(list_downoids)
	list_points_to_detect = np.float32(list_downoids).reshape(-1, 1, 2)
	# print("points to detect")
	# print (list_points_to_detect)
	transformed_points = cv2.perspectiveTransform(list_points_to_detect, matrix)
	# print("transform")
	# print(transformed_points)
	# Loop over the points and add them to the list that will be returned
	transformed_points_list = list()
	for i in range(0,transformed_points.shape[0]):
		transformed_points_list.append([transformed_points[i][0][0],transformed_points[i][0][1]])
	# print("transform_list")
	# print(transformed_points_list)
	return transformed_points_list