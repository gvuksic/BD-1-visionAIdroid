# BD1 LEGO servo M5Stack controller
# Author: Goran Vuksic

import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)

# servo motor is connected on pin 8
GPIO.setup(8, GPIO.OUT)

servo=GPIO.PWM(8, 50)
servo.start(0)
sleep(1)

# left (-90 deg position)
servo.ChangeDutyCycle(5)
sleep(1)

# neutral position
servo.ChangeDutyCycle(7.5)
sleep(1)

# right (+90 deg position)
servo.ChangeDutyCycle(10)
sleep(1)

# stop and cleanup
servo.stop()
GPIO.cleanup()
