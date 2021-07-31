import cv2 
import numpy as np
from numpy.lib.function_base import disp
import tensorflow as tf
from tensorflow.keras.models import load_model
from GUI import HandRecogGUI


# initilalize preprossing.
minRange = np.array([0, 133, 77], np.uint8)
maxRange = np.array([235, 173, 127], np.uint8)
def preprocess (image):
    YCRImage = cv2.cvtColor(image, cv2.COLOR_BGR2YCR_CB)
    skinArea = cv2.inRange(YCRImage, minRange, maxRange)
    return cv2.resize(skinArea, (320, 120))

def majority_black (image):
    black = np.where(
        (image[:] == 0) 
    )[0]
    return black.size / (320 * 120)

def loadModel(jsonStr, weightStr):
    json_file = open(jsonStr, 'r')
    loaded_nnet = json_file.read()
    json_file.close()

    serve_model = tf.keras.models.model_from_json(loaded_nnet)
    serve_model.load_weights(weightStr)

    serve_model.compile(optimizer='rmsprop',
                        loss='categorical_crossentropy',
                        metrics=['accuracy'])
    return serve_model

#GUI
gui = HandRecogGUI()

# init model
model = loadModel('model.json', 'model.h5')
print(model.summary())

# main loop (TODO: replace fist with Bunny hop! AND Find a better, faster way to move the mouse / keyboard! Finally, get confortable with using the gestures) try to replace bunny with some other gesture (v1 or v2 seems good)
hand_gestures = {0: '08_three', 1: '02_l', 2: '09_c', 3: '04_two', 4: '03_bunny', 5: '10_down', 6: '06_index', 7: '07_ok', 8: '05_thumb', 9: '01_palm'}
vc = cv2.VideoCapture(0)
if vc.isOpened(): # try to get the first frame
    rval, no_precessing_frame = vc.read()
    frame = preprocess(no_precessing_frame)
else:
    rval = False
prediction = ""
while rval:
    # process image and get NN output
    rval, no_precessing_frame = vc.read()
    frame = preprocess(no_precessing_frame)
    if majority_black(frame) < 0.99: # if a good amount of pixels is black, then that means there are no symbols. So we don't have to predict. 
        arr = np.array([frame]).reshape((1, 120, 320, 1)) / 255
        prediction = hand_gestures[np.argmax(model.predict(arr))]
    else:
        prediction = "None"
        gui.reset_last_action()
    
    # update pygame window
    if gui.draw(frame, prediction):
        vc.release()
        exit(0)