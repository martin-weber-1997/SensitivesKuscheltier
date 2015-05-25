import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
GPIO.output(11,True)
GPIO.output(13,True)
GPIO.output(15, True)
try:
	while True:
		time.sleep(1)
except KeyboardInterrupt:
	pass
GPIO.cleanup()
