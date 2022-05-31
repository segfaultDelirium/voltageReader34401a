#
# A.Skoczen, AGH0-UST
# Created: 04.2021
# multimetr agilent 34401a -> RS-232 -> FTDI -> USB -> pyftdi
# przyklad poprawnego rozwiazania pracy sygnalow DSR, DTR
# Developed: 31/05.2021
#
import pyftdi.serialext
import time
import os, sys, platform
import struct
import readVoltageLib


readVoltageLib.assertLinux()
readVoltageLib. assertPython3()

port = pyftdi.serialext.serial_for_url(url='ftdi://ftdi:232:FT4T6R2Q/1', baudrate=9600, timeout=10, bytesize=8, stopbits=2, parity='N')#, xonxoff=False, rtscts=False, dsrdtr=True)
readVoltageLib.initial(port)

while True :
    userInput = input("digit to start, letter to end")
    print("You entered: ", userInput)
    if not userInput.isdigit():
        print('ending...')
        break;
    print('starting...')
    voltageReceived = readVoltageLib.readAverageVoltage(port, True)
    print(voltageReceived)

remote = "SYST:LOC\n"
port.write(remote)
"""
"""
