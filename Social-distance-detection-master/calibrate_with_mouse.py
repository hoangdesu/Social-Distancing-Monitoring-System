import cv2
import numpy as np
import yaml
import imutils

 
 #TODO: NAM
# Define the callback function that we are going to use to get our coordinates
def CallBackFunc(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print("Left button of the mouse is clicked - position (", x, ", ",y, ")")
        list_points.append([x,y])
        ### NEW
        cv2.circle(img, (x, y), 5, (0, 255, 255), 5)
        ### NEW

video_name = "site_test_1.mp4"

size_frame = 600

vs = cv2.VideoCapture(video_name)
# vs = cv2.VideoCapture(video_name)

# Loop until the end of the video stream
while True:    
    # Load the frame and test if it has reache the end of the video
    (frame_exists, frame) = vs.read()
    frame = imutils.resize(frame, width=int(size_frame))
    cv2.imwrite("static_frame_from_video.jpg",frame)
    break

# Create a black image and a window
windowName = 'MouseCallback'
cv2.namedWindow(windowName)


# Load the image 
img_path = "static_frame_from_video.jpg"
img = cv2.imread(img_path)

# Get the size of the image for the calibration
height,width,_ = img.shape
print(height,width)

# Create an empty list of points for the coordinates
list_points = list()

# bind the callback function to window
cv2.setMouseCallback(windowName, CallBackFunc)


if __name__ == "__main__":
    # Check if the 4 points have been saved
    while (True):
        cv2.imshow(windowName, img)
        if len(list_points) == 6:
            # Return a dict to the YAML file
            config_data = dict(
                image_parameters = dict(
                    p1 = list_points[0],
                    p2 = list_points[1],
                    p3 = list_points[2],
                    p4 = list_points[3],
                    ### NEW
                    p5 = list_points[4],
                    p6 = list_points[5],
                    ### NEW
                    width_og = width,
                    height_og = height,
                    img_path = img_path,
                    size_frame = size_frame,
                    ))
            # Write the result to the config file
            with open('config_birdview.yml', 'w') as outfile:
                yaml.dump(config_data, outfile, default_flow_style=False)
            break
        if cv2.waitKey(20) == 27:
            break
    cv2.destroyAllWindows()