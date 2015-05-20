__author__ = 'Martin Weber'

from threading import Thread


class minion(Thread):
    def __init__(self):
        Thread.__init__(self)
