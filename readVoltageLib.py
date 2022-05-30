import pyftdi.serialext
import time
import os, sys, platform
import struct  

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

def initial(port, debug=False):
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

def readAverageVoltage(port, debug = False, seconds = 0.5):
    avg = 0.0
    sampleAmount = seconds/0.05
    for i in range( int(sampleAmount)):
        avg += readVoltage(port, debug)
    return avg / sampleAmount 

def readVoltage(port, debug=False):
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
    time.sleep(0.05)
    if data[-1] != '\n' : 
        data = data + port.read(2024)
    port.dtr = False
    if debug : print('-', data)
    return float(data)
