__author__ = 'Martin Weber'

from threading import Thread


# LED 3 beliebige GPIOS
LED1 = 11
LED2 = 13
LED3 = 15


#Helligkeitssensor 1 beliebiger GPIO Pin
BRIGHTNESS = 16

#Taster linke Hand
LH = 18

#Taster rechte Hand
RH = 22


class TemperatureValues(Thread):

    def __init__(self):
        Thread.__init__(self)


class AdxlValues(Thread):
    def _init_self(self):
        Thread.__init__(self)


class NFCReader(Thread):
    def __init__(self):
        Thread.__init__(self)


class Buttons(Thread):
    def __init__(self):
        Thread.__init__(self)


class MovementValues(Thread):
    def __init__(self):
        Thread.__init__(self)


class BrightnessValues(Thread):
    def __init__(self):
        Thread.__init__(self)


class LED(object):
    def __init__(self):


class Sounds(object):


