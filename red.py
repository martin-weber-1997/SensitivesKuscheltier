import RPi.GPIO as GPIO
import logging, time
GPIO.cleanup() 
GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BOARD) 
GPIO.setup(11, GPIO.OUT)  
GPIO.setup(15, GPIO.OUT) 
c1 = GPIO.PWM(11, 50) 
c3 = GPIO.PWM(15, 50) 
c1.start(0) 
c3.start(0) 
try:
    while True:
        for dc in range(0,101,1):
            c1.ChangeDutyCycle(dc)
            time.sleep(0.1)
        for dc in range(100,-1,-1):
            c1.ChangeDutyCycle(dc)
            time.sleep(0.1)
except KeyboardInterrupt:
    pass 
c1.stop()  
c3.stop() 
GPIO.cleanup()
