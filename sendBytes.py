# Enable pyserial extensions
import pyftdi.serialext


count = 0
# Open a serial port on the second FTDI device interface (IF/2) @ 3Mbaud
brate = 230400
#115200
#9600
#230400
#shockley
#url  = 'ftdi://ftdi:232:AB0K3Q4S/1'
#UBUNTU at home
url = 'ftdi://ftdi:232:AQ00RVND/1'
port = pyftdi.serialext.serial_for_url(url, baudrate=brate, bytesize=8, stopbits=1, parity='N', xonxoff=False, rtscts=False)


DAC_resolution = 2**12 -1 #4095

def voltageToBytesArray(voltage):
    voltageInDAC_resulution = int((voltage/2.5) * DAC_resolution)
#    data = voltageInDAC_resulution.to_bytes(2, 'little')
    first_byte = voltageInDAC_resulution.to_bytes(2, 'little')[1]
    second_byte =  voltageInDAC_resulution.to_bytes(2, 'little')[0]
    print(f'data= ', data)
    return bytes([0x80 + len(data), first_byte, second_byte, 0x80])



# Send bytes
print("Transmition at", brate)
#data = [0x32, 0x4c, 0x31, 0x36, 0x35, 0x37]
dac_value = 723
data = dac_value.to_bytes(2, 'big')
print(f'data= ', data)
fullLength = 0xc0 + len(data)
#b = bytes([0x80 + len(data), *data,  0x80, fullLength])
b = voltageToBytesArray(2.11)
print("-", b)
port.write(b)

# Receive bytes
nb = len(data)
print("Receiving at", brate)
print(nb, "bytes")
#data = port.read(nb)
print('-', data)

#
