import cv2
import time
import numpy as np

# Load the mount image
mount = cv2.imread('mount.png')

# Resize the mount image to match the size of the video frame
mount = cv2.resize(mount, (640, 480))

# Starting the webcam
cap = cv2.VideoCapture(1)

# Allowing the webcam to start by making the code sleep for 2 seconds
time.sleep(3)
bg = 0
print("Starting to capture the background.")
# Capturing background for 60 frames
for i in range(60):
    ret, bg = cap.read()
# Flipping the background
bg = np.flip(bg, axis=1)
print("Background Captured.")
# Reading the captured frame until the camera is open
while (cap.isOpened()):
    ret, img = cap.read()
    if not ret:
        break
    # Flipping the image for consistency
    img = np.flip(img, axis=1)

    # Converting the color from BGR to HSV
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Generating mask to detect red colour(values can be changed)
    lower_red = np.array([100,100,100])
    upper_red = np.array([255,255,255])
    mask_1 = cv2.inRange(rgb, lower_red, upper_red)
    
    mask = cv2.bitwise_not(mask_1) #this will sharpen the image by converting 0s to 1s and vice-versa

    # Keeping only the part of the images without the red color 
    #(or any other color you may choose)
    person = cv2.bitwise_and(img,img,mask=mask)

    # Generating the final output
    final_output = np.where(person==0,mount,person)

    # Displaying the output to the user
    cv2.imshow("Mountain Filter", final_output)
    code = cv2.waitKey(1)
    if code == 32:
        break

cap.release()
cv2.destroyAllWindows()
