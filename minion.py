# coding=utf-8
__author__ = 'Martin Weber'


# Teils Code von Erhard List, Walter Rafeiner-Magor benutzt

from time import sleep
from threading import Thread

import RPi.GPIO as GPIO
from adxl345 import ADXL345
from mf2 import NFCReader
import os

MODE = None
TEMP = None
ADXL = None
READER = None
IFR = None
BRIGHT = None






# LED 3 beliebige GPIOS
LED1 = 11
LED2 = 13
LED3 = 15



# Taster linke Hand
LH = 36

# Taster rechte Hand
RH = 37

# Begegungssensor
PIR = 16

#Temperatursensor
TMP = 7


class TemperatureValues(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.closed = False
        self.stopped = True
        self.run()

    def run(self):
        while not self.closed:
            while not self.stopped and not self.closed:
                #Farben ausgeben
                self.checkTemp()

    def checkTemp(self):
        #Farben ausgeben mit Temperatur
        print"Farbe ausgeben"

class Mode(object):
    def __init__(self):
        self.mode = 0
        self.long_pressed = 1

    def change(self):
        self.mode = (self.mode + 1) % 5

    def increase(self):
        self.long_pressed += 1


class AdxlValues(Thread):
    def _init_self(self):
        Thread.__init__(self)
        self.adxl = ADXL345()
        self.stopped = True
        self.closed = False
        self.x, self.y, self.z = 0, 0, 0
        self.start()

    def run(self):
        while not self.closed:
            while not self.closed and not self.stopped:
                self.checkValues()
                sleep(3)

    def checkValues(self):
        # Werte muessen noch probiert werden welche Richtig sind
        grenze = 0.2
        grenze2 = 1
        self.x, self.y, self.z = self.adxl.getAxes(True)['x'], self.adxl.getAxes(True)['y'], self.adxl.getAxes(True)[
            'z']
        while True:
            if (self.x > grenze or self.y > grenze or self.z > grenze):
                # Sound abspielen
                playSounds('Haha')
            elif (self.x > grenze2 or self.y > grenze2 or self.z > grenze2):
                # Anderen Sound abspielen
                playSounds('Stopa')


class NFCReader(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.reader = NFCReader()
        self.stopped = True
        self.closed = False
        self.start()

    def run(self):
        while not self.closed:
            while not self.closed and not self.stopped:
                if (GPIO.input(LH) == GPIO.HIGH):
                    print"Hand gedrueckt"
                    sound = self.reader.run()
                    playSounds(sound)
                    sleep(3)
                sleep(0.1)
                print"Test"


class Infrarot(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.stopped = True
        self.closed = False
        self.start()

    def run(self):
        while not self.closed:
            while not self.closed and not self.stopped:
                if (GPIO.input(PIR) == GPIO.HIGH):
                    playSounds("HelloPapagena")
                    sleep(10)


class BrightnessValues(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.stopped = True
        self.closed = False
        self.start()

    def run(self):
        while not self.closed:
            while not self.closed and not self.stopped:
                self.checkBrightness()

    def checkBrightness(self):
        #Wenn helligkeit unter X
        playSounds("Hello")
        print"Helligkeit"
        sleep(5)


def playSounds(self, sound):
    if (sound == "ahh"):
        mixer.music.load("/home/team1/Audio/Ahh")
        mixer.music.play()
    elif (sound == "401f8231"):
        #Apfel
        #mixer.music.load("/home/team1/Audio/Bappel")
        #mixer.music.play()
        os.system('sudo omxplayer --amp 2000 /home/team1/Audio/Bappel/1.wav')

    elif (sound == "5dd2b12b"):
        #Kiwi
        #mixer.music.load("/home/team1/Audio/Kiwi")
        #mixer.music.play()
        os.system('sudo omxplayer --amp 2000 /home/team1/Audio/Kiwi/1.wav')
    elif (sound == "443fa822"):
        #Orange
        #mixer.music.load("/home/team1/Audio/Oranja")
        #mixer.music.play()
        os.system('sudo omxplayer --amp 2000 /home/team1/Audio/Oranja/1.wav')
    elif (sound == "b5e69220"):
        #Banane
        #mixer.music.load("/home/team1/Audio/Banana")
        #mixer.music.play()
        os.system('sudo omxplayer --amp 2000 /home/team1/Audio/Banana/1.wav')
    elif (sound == "cd2bb22b"):
        #Melon
        #mixer.music.load("/home/team1/Audio/Melon")
        #mixer.music.play()
        os.system('sudo omxplayer --amp 2000 /home/team1/Audio/Melon/1.wav')
    elif (sound == ""):
        #NFC nicht erkannt
        #mixer.music.load("/home/team1/Audio/What")
        #mixer.music.play()
        os.system('sudo omxplayer --amp 2000 /home/team1/Audio/What/1.wav')
    elif (sound == "Hello"):
        #mixer.music.load("/home/team1/Audio/Hello")
        #mixer.music.play()
        os.system('sudo omxplayer --amp 2000 /home/team1/Audio/Hello/1.wav')
    elif (sound == "Popo"):
        #mixer.music.load("/home/team1/Audio/Popo")
        #mixer.music.play()
        os.system('sudo omxplayer --amp 2000 /home/team1/Audio/Popo/1.wav')
    elif (sound == "TaDaa"):
        #mixer.music.load("/home/team1/Audio/TaDaa")
        #mixer.music.play()
        os.system('sudo omxplayer --amp 2000 /home/team1/Audio/TaDaa/1.wav')
    elif (sound == "beeDo"):
        #mixer.music.load("/home/team1/Audio/beeDo")
        #mixer.music.play()
        os.system('sudo omxplayer --amp 2000 /home/team1/Audio/beeDo/1.wav')
    elif (sound == "Haha"):
        #mixer.music.load("/home/team1/Audio/Haha")
        #mixer.music.play()
        os.system('sudo omxplayer --amp 2000 /home/team1/Audio/Haha/1.wav')
    elif (sound == "HelloPapagena"):
        #mixer.music.load("/home/team1/Audio/HelloPapagena")
        #mixer.music.play()
        os.system('sudo omxplayer --amp 2000 /home/team1/Audio/HelloPapagena/1.wav')
    elif (sound == "Poopaye"):
        #mixer.music.load("/home/team1/Audio/Stopa")
        #mixer.music.play()
        os.system('sudo omxplayer --amp 2000 /home/team1/Audio/Stopa/1.wav')


#
#Methode noch nicht vollständig
#
#
#
def button_pressed(channel):
    # if BUTTON was rising
    print"Methode Aufgerufen"
    if GPIO.input(RH) == GPIO.HIGH:
        MODE.increase()
        print"Test"
    else:
        # change to next mode
        MODE.change()
    # if button was long pressed for four times:
    if MODE.long_pressed >= 4:
        #herrunterfahren
        print"Herrunterfahren"

    if MODE.mode == 1:
        #stop Brightness
        BRIGHT.stopped = True
        #Infrarot Sensor
        IFR.stopped = False

    elif MODE.mode == 2:
        #LOG.info("Schalte in Modus " + str(MODE.mode) + "LP: " + str(MODE.long_pressed))
        # stop Infrarot
        IFR.stopped = True
        #start ADXL
        ADXL.stopped = False

    elif MODE.mode == 3:
        #LOG.info("Schalte in Modus " + str(MODE.mode) + "LP: " + str(MODE.long_pressed))
        # stop ADXL
        ADXL.stopped = True
        #start NFC
        READER.stopped = False
    elif MODE.mode == 4:
        #Stop NFC
        READER.stopped = True
        #Start brightness
        BRIGHT.stopped = False
    elif MODE.mode == 0:
        BRIGHT.stopped=True


def init():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(LED1, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(LED2, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(LED3, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(PIR, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(RH, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(LH, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(RH, GPIO.BOTH, callback=button_pressed, bouncetime=800)


if __name__ == "__main__":
    MODE = Mode()
    TEMP = TemperatureValues()
    ADXL = AdxlValues()
    READER = NFCReader()
    IFR = Infrarot()
    BRIGHT = BrightnessValues()
    init()

try:
    while True:  # endless looping
        pass
except KeyboardInterrupt:
    TEMP.closed = True
    MODE.closed = True
    ADXL.closed = True
    READER.closed = True
    IFR.closed = True
    BRIGHT.closed = True
    # give me time to close all threads
    sleep(1)
finally:
    closeGPIO()

