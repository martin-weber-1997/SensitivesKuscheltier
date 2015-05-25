import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(16, GPIO.IN)
try:
	while True:
		print(GPIO.input(16))
		time.sleep(0.5)
except KeyboardInterrupt:
	GPIO.cleanup()
