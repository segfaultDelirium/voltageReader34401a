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

#check platform :
opsys = platform.system()
opsrel = platform.release()
print(opsys, opsrel)
if opsys != 'Linux':
    print("Wrong operating system")
    sys.exit()
#check python 3 :
pyth_ver = str(sys.version_info.major) + '.' + str(sys.version_info.minor) + '.' + str(sys.version_info.micro)
print('Python', pyth_ver)
if sys.version_info.major != 3:
    print("Wrong python version")
    sys.exit()

debug = True   
data = "HEWLETT-PACARD HEWLETT-PACARD HEWLETT-PACARD "
brate = 9600
#url = "ftdi://ftdi:232:FT4T6R2Q/1"
# url = "ftdi://ftdi:232:FT4Q20IC/1"
url = 'ftdi://ftdi:232:FT4T6R2Q/1'
port = pyftdi.serialext.serial_for_url(url, baudrate=brate, timeout=10, bytesize=8, stopbits=2, parity='N')
#, xonxoff=False, rtscts=False, dsrdtr=True)

LSB = 3.3/2**8
f = open("dac_tf.txt", "w")
f.write("Number\tValue raw [V]\tValue float [V]\tDigital [LSB]\tCode\n")

port.write(b'\x03')
time.sleep(1)
if debug : print("Initial DSR: ", port.dsr)
remote = "SYST:REM\n"
port.write(remote)
if debug : print("After remote DSR: ", port.dsr)
#beep = "SYST:BEEP\n"
#port.write(beep)
#disp = "DISP:TEXT \"AGH WFiIS\"\n"
#port.write(disp)
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
var = ''
next = True
while next :
    digit = False
    while not digit: 
        var = input("Please enter code: ")
        print("You entered: ", var, 'Transmition...')
        if var.isdigit() : 
            digit = True 
    if int(var) < 256 :
        for i in range(1,5):
            #time.sleep(1)
            qval = "READ?\n"
            if debug : print("DSR befor read:", port.dsr)
            port.write(qval)
            if debug : print("DSR after read: ", port.dsr)
            while port.dsr:
                pass
                #time.sleep(0.1)
            if debug : print("DSR after loop: ", port.dsr)
            # Important !!!!!!
            port.dtr = True
            data = port.read(2024)
            #time.sleep(1)
            if data[-1] != '\n' : 
                data1 = port.read(2024)
                data = data + data1
            port.dtr = False
            if debug : print(i, '-', data)
            # line = f'{data=}'

            data = data[0:-3] # sanitize the data
            print(f'{data=}')
            line = "%d\t%s\t%f\t%f\t%s\n" % (i, data, float(data), float(data)/LSB, var)
            f.write(line)
            print(line, end='')
    else:
        next = False
        print("Too big value:", var)
remote = "SYST:LOC\n"
port.write(remote)
f.close()
"""
"""
