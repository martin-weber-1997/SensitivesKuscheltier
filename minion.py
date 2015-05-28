# coding=utf-8
__author__ = 'Martin Weber'


# Teils Code von Erhard List, Walter Rafeiner-Magor benutzt

from time import sleep
import time
from threading import Thread
import logging
import RPi.GPIO as GPIO
from adxl345 import ADXL345
from mf2 import NFCReader
import os
import glob
from TSL2561 import TSL2561

MODE = None
TEMP = None
ADXL = None
READER = None
IFR = None
BRIGHT = None
PWMR=None
PWMG=None
PWMB=None
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
BASE_DIR = '/sys/bus/w1/devices/'
DEVICE_FOLDER = glob.glob(BASE_DIR + '28*')[0]
DEVICE_FILE = DEVICE_FOLDER + '/w1_slave'




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
        self.temp=read_ext_temp()
        self.start()

    def run(self):
        while not self.closed:
            while not self.stopped and not self.closed:
                #Farben ausgeben
                self.checkTemp()

            sleep(0.001)
            if(read_cpu_temp()>60):
                playSounds("beeDo")
                sleep(5)
                os.system("shutdown now -h")

    def checkTemp(self):
        #Farben ausgeben mit Temperatur
        tmp=read_ext_temp()-self.temp
        print tmp
        r= 100 if tmp>=0 else abs(tmp)*5
        g= 100-abs(tmp)*5
        b= 100 if tmp<=0 else abs(tmp)*5
        setLeds(r,g,b)


class Mode(object):
    def __init__(self):
        self.mode = 0
        self.long_pressed = 1

    def change(self):
        self.mode = (self.mode + 1) % 6

    def increase(self):
        self.long_pressed += 1


class AdxlValues(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.adxl = ADXL345()
        self.stopped = True
        self.closed = False
        self.x, self.y, self.z = 0, 0, 0
        self.xold, self.yold, self.zold = 0, 0, 0
        self.start()

    def run(self):
        while not self.closed:
            while not self.closed and not self.stopped:
                print"Schleife"
                self.checkValues()
                sleep(0.1)

    def checkValues(self):
        print"Test"
        # Werte muessen noch probiert werden welche Richtig sind
        grenze = 0.3
        grenze2 = 0.6
        self.x, self.y, self.z = self.adxl.getAxes(True)['x'], self.adxl.getAxes(True)['y'], self.adxl.getAxes(True)['z']
        print " X= %.2f Y= %.2f Z= %.2f" % (self.x,self.y,self.z)
        print " X2= %.2f Y2= %.2f Z2= %.2f" % (self.xold,self.yold,self.zold)

        if (abs(self.x) > abs(self.xold)+grenze or abs(self.y) > abs(self.yold)+grenze or abs(self.z) > abs(self.zold)+grenze):
            # Sound abspielen
            playSounds('Haha')
        elif (abs(self.x) > abs(self.xold)+grenze2 or abs(self.y) > abs(self.yold)+grenze2 or abs(self.z) > abs(self.zold)+grenze2):
            # Anderen Sound abspielen
            playSounds('Stopa')
        self.xold, self.yold, self.zold = self.x, self.y, self.z


class Reader(Thread):
    def __init__(self):
        logger = logging.getLogger("cardhandler").info
        Thread.__init__(self)
        self.reader = NFCReader(logger)
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
        self.br=TSL2561()
        self.start()

    def run(self):
        while not self.closed:
            while not self.closed and not self.stopped:
                self.checkBrightness()
                sleep(0.1)

    def checkBrightness(self):
        if(self.br.readLux()<1):
            playSounds("Hello")
            sleep(5)


def playSounds(sound):
    if (sound == "ahh"):
        os.system('sudo omxplayer --amp 2000 /home/team1/Audio/Ahh/1.wav')
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
    if GPIO.input(RH) == GPIO.LOW:
        MODE.increase()
    else:
        # change to next mode
        MODE.change()
    # if button was long pressed for four times:
    if MODE.long_pressed >= 4:
        #herrunterfahren
        print"Herrunterfahren"

    if MODE.mode == 1:
        playSounds("Popo")
        sleep(1)
        #stop Brightness
        BRIGHT.stopped = True
        #Infrarot Sensor
        IFR.stopped = False
        print"Infrarot"

    elif MODE.mode == 2:
        playSounds("Popo")
        sleep(1)
        #LOG.info("Schalte in Modus " + str(MODE.mode) + "LP: " + str(MODE.long_pressed))
        # stop Infrarot
        IFR.stopped = True
        #start ADXL
        ADXL.stopped = False
        print"ADXL"

    elif MODE.mode == 3:
        playSounds("Popo")
        sleep(1)
        #LOG.info("Schalte in Modus " + str(MODE.mode) + "LP: " + str(MODE.long_pressed))
        # stop ADXL
        ADXL.stopped = True
        #start NFC
        READER.stopped = False
        print"NFC"
    elif MODE.mode == 4:
        playSounds("Popo")
        sleep(1)
        #Stop NFC
        READER.stopped = True
        #Start brightness
        BRIGHT.stopped = False
        print"Bright"
    elif MODE.mode == 5:
        playSounds("Popo")
        sleep(1)
        #stop Bright
        BRIGHT.stopped=True
        #start Temp
        TEMP.stopped=False
        print"temp"
    elif MODE.mode == 0:
        playSounds("Popo")
        sleep(1)
        TEMP.stopped=True
        setLeds(100,100,100)
        print"leerlauf"

def setLeds(r,g,b):
    PWMR.ChangeDutyCycle(r)
    PWMG.ChangeDutyCycle(g)
    PWMB.ChangeDutyCycle(b)

def init():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(LED1, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(LED2, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(LED3, GPIO.OUT, initial=GPIO.LOW)

    GPIO.setup(PIR, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(RH, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(LH, GPIO.IN ,pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(RH, GPIO.BOTH, callback=button_pressed, bouncetime=800)

def read_temp_raw():
    f = open(DEVICE_FILE, 'r')
    lines = f.readlines()
    f.close()
    return lines
def read_ext_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp = float(temp_string) / 1000.0
        return temp
def read_cpu_temp():
  f = open('/sys/class/thermal/thermal_zone0/temp', 'r')
  cpu_temp_raw = f.read()
  f.close()
  return float(cpu_temp_raw) / 1000.0

if __name__ == "__main__":


    MODE = Mode()
    TEMP = TemperatureValues()
    ADXL = AdxlValues()
    READER = Reader()
    IFR = Infrarot()
    BRIGHT = BrightnessValues()
    init()
    PWMR = GPIO.PWM(LED1, 1000)
    PWMG = GPIO.PWM(LED2, 1000)
    PWMB = GPIO.PWM(LED3, 1000)
    PWMR.start(0)
    PWMG.start(0)
    PWMB.start(0)

    setLeds(0,100,0)
    sleep(1)
    setLeds(100,100,100)


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
    PWMR.stop()
    PWMG.stop()
    PWMB.stop()
    # give me time to close all threads
    sleep(1)

finally:
    GPIO.cleanup()

