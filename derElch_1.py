__author__ = 'Erhard List, Walter Rafeiner-Magor'

import logging
from time import sleep
import os
from threading import Thread

import RPi.GPIO as GPIO
from SensitivesKuscheltier.adxl345 import ADXL345




###########################
# for remote debugging only
# import pydevd
# use your own host ip-address
# pydevd.settrace('172.22.172.83', port=55555, stdoutToServer=True, stderrToServer=True)
###########################

# Set logging to level INFO
logging.basicConfig(level=logging.INFO)

# static variables
# !!!!!! BCM numbering !!!!!!!
HORN_RE_GRUEN = 9
HORN_RE_GELB = 6
HORN_RE_ROT = 10
HORN_LI_GRUEN = 26
HORN_LI_GELB = 13
HORN_LI_ROT = 19
PIR = 5
BUTTON = 11

# instance of class Mode
MODE = None
# instance of thread RunLeds
RUNNING_LEDS = None
# instance of thread AdxlRun
ADXL_RUN = None

LOG = logging.getLogger(__name__)


class RunLeds(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.stopped = True
        self.closed = False
        self.start()

    def run(self):
        while self.closed == False:
            while not self.closed and not self.stopped:
                GPIO.output(HORN_RE_GRUEN, GPIO.HIGH)
                sleep(0.1)
                GPIO.output(HORN_RE_GRUEN, GPIO.LOW)
                GPIO.output(HORN_RE_GELB, GPIO.HIGH)
                sleep(0.1)
                GPIO.output(HORN_RE_GELB, GPIO.LOW)
                GPIO.output(HORN_RE_ROT, GPIO.HIGH)
                sleep(0.1)
                GPIO.output(HORN_RE_ROT, GPIO.LOW)
                GPIO.output(HORN_LI_ROT, GPIO.HIGH)
                sleep(0.1)
                GPIO.output(HORN_LI_ROT, GPIO.LOW)
                GPIO.output(HORN_LI_GELB, GPIO.HIGH)
                sleep(0.1)
                GPIO.output(HORN_LI_GELB, GPIO.LOW)
                GPIO.output(HORN_LI_GRUEN, GPIO.HIGH)
                sleep(0.1)
                GPIO.output(HORN_LI_GRUEN, GPIO.LOW)


def resetLEDs():
    GPIO.output(HORN_RE_GELB, GPIO.LOW)
    GPIO.output(HORN_LI_GELB, GPIO.LOW)
    GPIO.output(HORN_RE_GRUEN, GPIO.LOW)
    GPIO.output(HORN_LI_GRUEN, GPIO.LOW)
    GPIO.output(HORN_RE_ROT, GPIO.LOW)
    GPIO.output(HORN_LI_ROT, GPIO.LOW)


def my_callback(channel):
    # if PIR was falling
    if GPIO.input(PIR) == GPIO.LOW:
        RUNNING_LEDS.stopped = True
    else:
        RUNNING_LEDS.stopped = False


class Mode(object):
    def __init__(self):
        self.mode = 0
        self.long_pressed = 1

    def increase(self):
        self.long_pressed += 1
        LOG.info("LP: " + str(self.long_pressed))

    def change(self):
        self.mode = (self.mode + 1) % 3


class AdxlRun(Thread):
    """ The Logger receives x, y, z from a adxl345
    and show a tuple  x, y, z as 6 LEDS
    """

    def __init__(self):
        """ Creates a new object for logging the adxl345 outputs
        """
        Thread.__init__(self)
        # the thread is paused
        self.stopped = True
        self.closed = False
        # create new instance of ADXL345 receiver
        LOG.info("create adxl345")
        self.a = ADXL345()
        # initialize the output values
        self.x, self.y, self.z = 0, 0, 0
        LOG.info("starting ADXL thread...")
        # start the thread
        self.start()

    def get_values(self):
        # iterate over data elements
        self.y, self.x, self.z = self.a.getAxes(True).values()

    def show_values(self):
        """ set the LEDs depending on our current situation
        """
        if self.x > 0:
            GPIO.output(HORN_RE_GRUEN, GPIO.LOW)
            GPIO.output(HORN_LI_GRUEN, GPIO.HIGH)
        elif self.x < 0:
            GPIO.output(HORN_LI_GRUEN, GPIO.LOW)
            GPIO.output(HORN_RE_GRUEN, GPIO.HIGH)
        if self.y > 0:
            GPIO.output(HORN_RE_GELB, GPIO.LOW)
            GPIO.output(HORN_LI_GELB, GPIO.HIGH)
        elif self.y < 0:
            GPIO.output(HORN_LI_GELB, GPIO.LOW)
            GPIO.output(HORN_RE_GELB, GPIO.HIGH)
        if self.z > 0:
            GPIO.output(HORN_RE_ROT, GPIO.LOW)
            GPIO.output(HORN_LI_ROT, GPIO.HIGH)
        elif self.z < 0:
            GPIO.output(HORN_LI_ROT, GPIO.LOW)
            GPIO.output(HORN_RE_ROT, GPIO.HIGH)

    def run(self):
        while not self.closed:
            while not self.closed and not self.stopped:
                self.get_values()
                self.show_values()
                sleep(0.3)


def button_pressed(channel):
    # if BUTTON was rising
    if GPIO.input(BUTTON) == GPIO.HIGH:
        MODE.increase()
    else:
        # change to next mode
        MODE.change()
    # if button was long pressed for four times:
    if MODE.long_pressed >= 4:
        shutdown()
    if MODE.mode == 1:
        LOG.info("Schalte in Modus " + str(MODE.mode) + "LP: " + str(MODE.long_pressed))
        # start runnig leds
        GPIO.add_event_detect(PIR, GPIO.BOTH, callback=my_callback, bouncetime=1000)
        RUNNING_LEDS.stopped = False

    elif MODE.mode == 2:
        LOG.info("Schalte in Modus " + str(MODE.mode) + "LP: " + str(MODE.long_pressed))
        # stop running leds
        RUNNING_LEDS.stopped = True
        GPIO.remove_event_detect(PIR)
        # start the acceleration sensor
        ADXL_RUN.stopped = False
    elif MODE.mode == 0:
        LOG.info("Schalte in Modus " + str(MODE.mode) + "LP: " + str(MODE.long_pressed))
        # stop accelertion sensor output
        ADXL_RUN.stopped = True
        # no operation
        resetLEDs()


def initialize():
    """ initialize the numbering system
    :return:
    """
    LOG.info("initialize ...")
    GPIO.setmode(GPIO.BCM)
    """ Pins herrichten """
    GPIO.setup(HORN_RE_GRUEN, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(HORN_RE_GELB, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(HORN_RE_ROT, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(HORN_LI_GRUEN, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(HORN_LI_GELB, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(HORN_LI_ROT, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(PIR, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    # add an event for button pressed
    GPIO.add_event_detect(BUTTON, GPIO.BOTH, callback=button_pressed, bouncetime=800)


def shutdown():
    # Shutdown
    os.system('shutdown now -h')


def closeGPIO():
    LOG.info("Elch geht jetzt schlafen")
    GPIO.cleanup()

# if __name__ == "__main__":
# create new thread instances
MODE = Mode()
RUNNING_LEDS = RunLeds()
ADXL_RUN = AdxlRun()
# initialize GPIOs and button event
initialize()
try:
    while True:  # endless looping
        pass
except KeyboardInterrupt:
    LOG.warning("\nProgram will be terminated!")
    RUNNING_LEDS.closed = True
    MODE.closed = True
    ADXL_RUN.closed = True
    # give me time to close all threads
    sleep(1)
finally:
    closeGPIO()
