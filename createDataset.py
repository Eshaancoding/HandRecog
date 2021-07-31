import cv2 
import numpy as np
import os
from math import floor

def get_section (i): 
    num = floor(10*(i / 2000))
    if i % 200 == 0 and i > 0: 
        num -= 1 
    return num
 
def number_to_string (number, num_of_digits):
    digit_count = 0
    Number = number
    while(Number > 0):
        Number = Number // 10
        digit_count = digit_count + 1
    if number == 0: 
        digit_count = 1
    str_digit = ""
    for _ in range(num_of_digits - digit_count):
        str_digit += "0"
    str_digit += str(number)
    return str_digit

# initilalize preprossing.
minRange = np.array([0, 133, 77], np.uint8)
maxRange = np.array([235, 173, 127], np.uint8)
def preprocess (image):
    YCRImage = cv2.cvtColor(image, cv2.COLOR_BGR2YCR_CB)
    skinArea = cv2.inRange(YCRImage, minRange, maxRange)
    return cv2.resize(skinArea, (320, 120))
# main loop
hand_gestures = {0: '02_l', 1: '04_two', 2: '09_c', 3: '10_down', 4: '06_index', 5: '08_three', 6: '07_ok', 7: '05_thumb', 8: '01_palm', 9: '03_bunny'}
cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)
if vc.isOpened(): # try to get the first frame
    rval, no_precessing_frame = vc.read()
    frame = preprocess(no_precessing_frame)
else:
    rval = False

################## IMAGE ####################
# All signs has been from the right hand
# Have done: 
# 0: 02_l 
# 1: 04_two 
# 2: 09_c
# 3: 10_down
# 4: 06_index (make sure your thumb is from the right side)
# 5: 08_three 
# 6: 07_ok  
# 7: 05_thumb
# 8: 01_palm
# 9: 03_bunny
image_index = 9
#############################################

i = 0
frame_count = 0
while rval:
    i += 1
    frame_count += 1
    if frame_count == 201:
        frame_count = 1
    cv2.imshow("preview", frame)
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break
    rval, no_precessing_frame = vc.read()
    frame = preprocess(no_precessing_frame)

    # save frame
    section = number_to_string(get_section(i),2)
    frame_path = "frame_"+section+"_"+hand_gestures[image_index][0:2]+"_"+number_to_string(frame_count,4)
    path = os.path.join(".\dataset", section, hand_gestures[image_index], frame_path+".png")
    print(path)
    cv2.imwrite(path, frame)
    if i == 2000:
        break

cv2.destroyAllWindows()
vc.release()