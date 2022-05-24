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

def assertLinux():
    #check platform :
    opsys = platform.system()
    opsrel = platform.release()
    print(opsys, opsrel)
    if opsys != 'Linux':
        print("Wrong operating system")
        sys.exit()

def assertPython3():
    #check python 3 :
    pyth_ver = str(sys.version_info.major) + '.' + str(sys.version_info.minor) + '.' + str(sys.version_info.micro)
    print('Python', pyth_ver)
    if sys.version_info.major != 3:
        print("Wrong python version")
        sys.exit()

def initial(port):
    port.write(b'\x03')
    time.sleep(1)
    if debug : print("Initial DSR: ", port.dsr)
    port.write("SYST:REM\n")
    if debug : print("After remote DSR: ", port.dsr)
    if debug : print("DSR after disp: ", port.dsr)
    # Important !!!!!!
    time.sleep(1)
    print('Wait...')
    id = "*IDN?\n"
    if debug : print("DSR befor id:", port.dsr)
    port.write(id)
    if debug : print("DSR after id: ", port.dsr)
    while port.dsr:
        pass
        #time.sleep(0.1)

    if debug : print("DSR after loop: ", port.dsr)
    # Important !!!!!!
    port.dtr = True
    data = port.read(2024)
    time.sleep(2)
    if data[-1] != '\n' : 
        data1 = port.read(2024)
        data = data + data1
    port.dtr = False
    print('Measurement instrument:', data)
    time.sleep(2)
    conf = "CONF:VOLT:DC 4,0.0001\n"
    port.write(conf)
    samp = "SAMP:COUN 1\n"
    port.write(samp)

def readVoltage(port):
    #time.sleep(1)
    if debug : print("DSR befor read:", port.dsr)
    port.write("READ?\n")
    if debug : print("DSR after read: ", port.dsr)
    while port.dsr:
        pass
        #time.sleep(0.1)
    if debug : print("DSR after loop: ", port.dsr)
    # Important !!!!!!
    port.dtr = True
    data = port.read(2024)
    time.sleep(1)
    if data[-1] != '\n' : 
        data = data + port.read(2024)
    port.dtr = False
    if debug : print('-', data)
    line = data
    # data = data[0:-3] # sanitize the data
    # print(f'after sanitizing: {data=}')

    # line = "%s\t%f\t%f\n" % (data, float(data), float(data)/LSB)
    print(line, end='')
    return data;

assertLinux()
assertPython3()

debug = True   
data = "HEWLETT-PACARD HEWLETT-PACARD HEWLETT-PACARD "
brate = 9600
url = 'ftdi://ftdi:232:FT4T6R2Q/1'
port = pyftdi.serialext.serial_for_url(url, baudrate=brate, timeout=10, bytesize=8, stopbits=2, parity='N')
#, xonxoff=False, rtscts=False, dsrdtr=True)
LSB = 3.3/2**8
initial(port)

next = True
while next :
    userInput = input("digit to start, letter to end")
    print("You entered: ", userInput)
    if not userInput.isdigit():
        print('ending...')
        next = False
        continue;
    print('starting...')
    readVoltage = readVoltage(port)

remote = "SYST:LOC\n"
port.write(remote)
"""
"""


# return error code -101 = invalid character