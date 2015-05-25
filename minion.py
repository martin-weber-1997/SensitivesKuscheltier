# coding=utf-8
__author__ = 'Martin Weber'

from time import sleep
from threading import Thread

import RPi.GPIO as GPIO
from SensitivesKuscheltier.adxl345 import ADXL345











# LED 3 beliebige GPIOS
LED1 = 11
LED2 = 13
LED3 = 15


# Helligkeitssensor 1 beliebiger GPIO Pin
BRIGHTNESS = 16

# Taster linke Hand
LH = 18

# Taster rechte Hand
RH = 22

# Helligkeitssensor
PIR = 36


class TemperatureValues(Thread):
    def __init__(self):
        Thread.__init__(self)


class AdxlValues(Thread):
    def _init_self(self):
        Thread.__init__(self)
        self.adxl = ADXL345()
        self.x ,self.y,self.z = self.adxl.getAxes(True)['x'],self.adxl.getAxes(True)['y'],self.adxl.getAxes(True)['z']
        self.checkValues()

    def checkValues(self):
        # Werte muessen noch probiert werden welche Richtig sind
        grenze = 0.2
        grenze2 = 1
        self.x ,self.y,self.z = self.adxl.getAxes(True)['x'],self.adxl.getAxes(True)['y'],self.adxl.getAxes(True)['z']
        while True:
            if (self.x > grenze or self.y > grenze or self.z > grenze):
                # Sound abspielen
                playSounds('lachen')
            elif (self.x > grenze2 or self.y > grenze2 or self.z > grenze2):
                # Anderen Sound abspielen
                playSounds('stop')


class NFCReader(Thread):
    def __init__(self):
        Thread.__init__(self)


class Buttons(Thread):
    def __init__(self):
        Thread.__init__(self)


def detectMovement(channel):
    if GPIO.input(PIR) == GPIO.HIGH:
        # Sound abspielen
        # Augen ändern?
        sleep(20)

    # Kommt noch in Methode ruft detectMovement auf falls Bewegungssensor ausschlaegt


GPIO.add_event_detect(PIR, GPIO.HIGH, callback=detectMovement(), bouncetime=1000)


class BrightnessValues(Thread):
    def __init__(self):
        Thread.__init__(self)


class LED(object):
    def __init__(self):
        self.r = 0
        self.g = 0
        self.b = 0

    def setColour(self):


# Farbe mit PWM setzen


def playSounds(self, sound):
    # Sound aufrufen


    def init():
        GPIO.setup(PIR, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(LED1, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(LED2, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(LED3, GPIO.OUT, initial=GPIO.LOW)

