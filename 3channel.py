""" Class libary for setting up three pins for RGB pwm """ __author__ = "Jeroen Bosch" __version__ = 0.1 
import RPi.GPIO as GPIO import logging GPIO.setmode(GPIO.BOARD) class RGB_PWM:
    __rbg = []
    __brightness = 1
    __color = []
    # init function
    def __init__(self, red, green, blue):
        GPIO.setup(red, GPIO.OUT)
        GPIO.setup(green, GPIO.OUT)
        GPIO.setup(blue, GPIO.OUT)
        c1 = GPIO.PWM(red, 100)
        c2 = GPIO.PWM(green, 100)
        c3 = GPIO.PWM(blue, 100)
        
        self.__rgb = [c1, c2, c3]
        logger.info("Initializing...")
    # a color setter, converts colors to DC for each color
    def changeColor(self, color):
        # save the new color for future reference
        self.__color = color
        # you can use the brightness to further change the DC
        r_dc = color[0] / 256 * 100
        g_dc = color[1] / 256 * 100
        b_dc = color[2] / 256 * 100
        # set the new DC
        self.__rgb[0].ChangeDutyCycle(r_dc)
        self.__rgb[1].ChangeDutyCycle(g_dc)
        self.__rgb[2].ChangeDutyCycle(b_dc)
    # a stop function
    def stop(self):
        for channel in self.rgb
            channel.stop()
    # a start function
    def start(self):
        for channel in self.rgb
            # start with full duty cycle
            channel.start(1)
    # set the brightness
    def setBrightness(self, level):
        self.brightness = level
        self.changeColor(self.color)
