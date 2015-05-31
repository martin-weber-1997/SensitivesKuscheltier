__author__ = 'Martin'
import RPi.GPIO as GPIO

RH = 37
global test
test = 0
def increase():
    test +=1

def button_pressed(channel):
    print"TEST"
    if GPIO.input(RH) == GPIO.HIGH:
        test += 1
        print"increase"
    else:
        print"change"

GPIO.setmode(GPIO.BOARD)
GPIO.setup(RH, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(RH, GPIO.BOTH, callback=button_pressed, bouncetime=800)
if __name__ == "__main__":
    test=0
    try:
        while True:  # endless l-ooping
          pass
    except KeyboardInterrupt:
       GPIO.cleanup()