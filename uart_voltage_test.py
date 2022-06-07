# to run the program: sudo python3 <filename>

# Enable pyserial extensions
import pyftdi.serialext
from numpy import arange
import time
import readVoltageLib

debug = False

def writeToFPGA(port, bytesArray, debug=False):
    if debug:
        pass
        #print('pretend to write to fpga...')
    else:
        port.write(bytesArray)

def readFromFPGA(port, amount, debug=False, expectedData='debug expected data'):
    if debug:
        return expectedData
    return port.read(amount)

def readFromSensor(port, debug=False, expectedData='debug expected data'):
    if debug:
        return expectedData
    return readVoltageLib.readAverageVoltage(port)

def getPort(url, debug, **kwargs):
    print(f'getPort args: {kwargs=}')
    if debug:
        return 'debug_port'
    return pyftdi.serialext.serial_for_url(url=url, **kwargs)

def voltageInDAC_resolutionToBin(voltage):
    return str(bin(voltage))




fpgaUrl = 'ftdi://ftdi:232:AB0K3Q4S/1' # to check the url, run the script `sudo python3 ftdi_urls.py`
sensorUrl = 'ftdi://ftdi:232:FT4T6R2Q/1'
# Open a serial port on the second FTDI device interface (IF/2) @ 3Mbaud
# available baud rates: 230400, 115200, 9600, 230400
fpgaPort = getPort(url=fpgaUrl, debug=debug, baudrate=230400, bytesize=8, stopbits=1, parity='N', xonxoff=False, rtscts=False)
# fpgaPort = pyftdi.serialext.serial_for_url(fpgaUrl, baudrate=230400, bytesize=8, stopbits=1, parity='N', xonxoff=False, rtscts=False) 
voltageReaderPort = getPort(url=sensorUrl, debug=debug, baudrate=9600, timeout=10, bytesize=8, stopbits=2, parity='N')#, xonxoff=False, rtscts=False, dsrdtr=True)
# voltageReaderPort = pyftdi.serialext.serial_for_url(url=sensorUrl, baudrate=9600, timeout=10, bytesize=8, stopbits=2, parity='N')#, xonxoff=False, rtscts=False, dsrdtr=True)
if not debug:
    readVoltageLib.initial(voltageReaderPort)

# Send bytes
helloString = "hello"
bytesArray = bytes([0x33, 0x35, 0x87, *bytes(helloString, 'ascii'), 0x80, 0xc6 ])
#b = bytes([0x33, 0x35, 0x87, 0x32, 0x4c, 0x31, 0x36, 0x35, 0x35, 0x37, 0x80, 0xc7])
print("-", bytesArray)
writeToFPGA(fpgaPort, bytesArray, debug)

minVoltage = 0.0
maxVoltage = 3.3
voltageStep = 0.1
DAC_resolution = 2**12 -1 #4095
for voltage in arange(minVoltage, maxVoltage + voltageStep, voltageStep):
    print()
    voltageInDAC_resulution = int((voltage/maxVoltage) * DAC_resolution)
    voltageBitsArray = str(bin(voltage))
    # voltageBitsArray = [voltageInDAC_resulution] #bytes(voltageInDAC_resulution)
    print(f'{voltage=}\t{voltageInDAC_resulution=}\t {voltageBitsArray=}')
    writeToFPGA(fpgaPort, voltageBitsArray, debug)
    time.sleep(0.1)
    fpgaVoltage = voltage
    fpgaVoltage = readFromFPGA(fpgaPort, len(voltageBitsArray), debug, expectedData=voltage)
    print(f'{fpgaVoltage=}')
    time.sleep(0.1)
    sensedVoltage = voltage
    sensedVoltage = readFromSensor(voltageReaderPort, debug, voltage);
    print(f'{sensedVoltage=}')
