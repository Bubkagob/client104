import sys
import os
from ctypes import util, CDLL, CFUNCTYPE, POINTER, c_void_p, c_char_p, c_int
from ctypes import c_bool

iec60870 = CDLL('./libiec60870.so')


class Client():
    def __init__(self, ip="127.0.0.1", port=2404):
        print(ip, port)
