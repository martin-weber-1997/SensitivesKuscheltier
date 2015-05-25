import RPi.GPIO as GPIO
import time
import os
GPIO.setmode(GPIO.BOARD)
GPIO.setup(5, GPIO.IN, pull_up_down = GPIO.PUD_UP)
while True:
	if(GPIO.input(5) == False):
		GPIO.setup(11, GPIO.OUT)
		GPIO.setup(13, GPIO.OUT)
		GPIO.setup(15, GPIO.OUT)
		c1 = GPIO.PWM(11, 1000)
		c2 = GPIO.PWM(13, 1000)
		c3 = GPIO.PWM(15, 1000)
		c1.start(0)
		c2.start(0)
		c3.start(0)
		i = 0
		while (i<3):
			for dc in range(0,101,5):
				c1.ChangeDutyCycle(dc)
				c2.ChangeDutyCycle(dc)
				c3.ChangeDutyCycle(dc)
				time.sleep(0.01)
			for dc in range(100,-1,-5):
				c1.ChangeDutyCycle(dc)
				c2.ChangeDutyCycle(dc)
				c3.ChangeDutyCycle(dc)
				time.sleep(0.01)
			i=i+1
		c1.stop()
		c2.stop()
		c3.stop()	
		GPIO.cleanup()
		os.system("sudo shutdown -h now 'System halted by a GPIO action'")
		break
	time.sleep(1)
