__author__ = 'Martin Weber'

from threading import Thread


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