import RPi.GPIO as GPIO
import logging, time
GPIO.cleanup() 
GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BOARD) 
GPIO.setup(11, GPIO.OUT)   
c1 = GPIO.PWM(11, 1000)
c1.start(0) 
try:
    while True:
    	c1.ChangeDutyCycle(0)
       	time.sleep(0.05)
        c1.ChangeDutyCycle(100)
        time.sleep(0.01)
except KeyboardInterrupt:
    pass 
c1.stop()  
GPIO.cleanup()
