# BD1 LEGO Controller
# Author: Goran Vuksic

import cv2
import RPi.GPIO as GPIO
from time import sleep
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials

# credentials for Azure Custom Vision
credentials = ApiKeyCredentials(in_headers={"Prediction-key": "<PREDICTION_KEY>"})
predictor = CustomVisionPredictionClient("<ENDPOINT_URL>", credentials)

GPIO.setmode(GPIO.BOARD)

# servo motor is connected on pin 8
GPIO.setup(8, GPIO.OUT)

# start servo
servo=GPIO.PWM(8, 50)
servo.start(0)
sleep(1)
# position it in neutral position
servo.ChangeDutyCycle(7.5)
sleep(0.5)
servo.ChangeDutyCycle(0)
sleep(0.5)

# camera
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

# positions: 0 - left, 1 - middle, 2 - right
currentposition = 1

try:
    while True:
        # store image
        ret, image = camera.read()
        cv2.imwrite('capture.png', image)

        with open("capture.png", mode="rb") as captured_image:
            results = predictor.detect_image("<PROJECT_ID>", "<ITERATION_NAME>", captured_image)

        for prediction in results.predictions:
            if prediction.probability > 0.5:
                print (prediction.bounding_box)
                locationBD1 = prediction.bounding_box.left + prediction.bounding_box.width / 2
                if locationBD1 < 0.3:
                    if currentposition != 0:
                        servo.ChangeDutyCycle(5)
                        currentposition = 0
                elif locationBD1 > 0.7:
                    if currentposition != 2:
                        servo.ChangeDutyCycle(10)
                        currentposition = 2
                elif locationBD1 > 0.3 and locationBD1 < 0.7:
                    if currentposition != 1:
                        servo.ChangeDutyCycle(7.5)
                        currentposition = 1
                sleep(0.5)
            servo.ChangeDutyCycle(0)
        # enable to store result as image with bounding box 
        #bbox = prediction.bounding_box
        #result_image = cv2.rectangle(image, (int(bbox.left * 640), int(bbox.top * 480)), (int((bbox.left + bbox.width) * 640), int((bbox.top + bbox.height) * 480)), (0, 255, 0), 3)
        #cv2.imwrite('result.png', result_image)

except KeyboardInterrupt:
    GPIO.cleanup()
    camera.release()
