#!/bin/python
import serial
import time
import sys
from struct import *

# data structure: https://github.com/avaldebe/AQmon/blob/master/Documents/PMS3003_LOGOELE.pdf
#          ttyUSB0:424d 1400 2500 2f00
debug = 0
class g3sensor():
    def __init__(self):
        self.endian = sys.byteorder

    def conn_serial_port(self, device):
        self.serial = serial.Serial(device, baudrate=9600, timeout=2)

    def check_keyword(self):
        currtime = int(time.time())
        while True and int(time.time()) - currtime < 4:
            if (self.serial.inWaiting()>0):
                token = self.serial.read(2)
                token_hex = token.hex()
                if token_hex == '424d':
                    return True
        return False

    def vertify_data(self, data):
        n = 2
        sum = int('42', 16) + int('4d', 16)
        for i in range(0, len(data) - 4, n):
            # print data[i:i+n]
            sum = sum + int(data[i:i + n], 16)
        versum = int(data[40] + data[41] + data[42] + data[43], 16)
        if sum == versum:
            print("data correct")

    def read_data(self):
        data = self.serial.read(22)
        data_hex = data.hex()
        if debug: self.vertify_data(data_hex)
        pm1_cf = int(data_hex[4] + data_hex[5] + data_hex[6] + data_hex[7], 16)
        pm25_cf = int(data_hex[8] + data_hex[9] + data_hex[10] + data_hex[11],
                      16)
        pm10_cf = int(data_hex[12] + data_hex[13] + data_hex[14] + data_hex[15],
                      16)
        pm1 = int(data_hex[16] + data_hex[17] + data_hex[18] + data_hex[19], 16)
        pm25 = int(data_hex[20] + data_hex[21] + data_hex[22] + data_hex[23],
                   16)
        pm10 = int(data_hex[24] + data_hex[25] + data_hex[26] + data_hex[27],
                   16)
        data = [pm1_cf, pm10_cf, pm25_cf, pm1, pm10, pm25]
        self.serial.close()
        return data

    def read(self, argv):
        tty = argv[0:]
        self.conn_serial_port(tty)
        if self.check_keyword() == True:
            data = self.read_data()
            return data
        self.serial.close()
        return [-1,-1,-1,-1,-1,-1]
