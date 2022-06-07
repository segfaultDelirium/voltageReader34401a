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
url = 'ftdi://ftdi:232:AB0K3Q4S/1'
port = pyftdi.serialext.serial_for_url(url, baudrate=brate, bytesize=8, stopbits=1, parity='N', xonxoff=False, rtscts=False)

# Send bytes
print("Transmition at", brate)
#data = [0x32, 0x4c, 0x31, 0x36, 0x35, 0x37]
dac_value = 4023
data = dac_value.to_bytes(2, 'big')
print(f'data= ', data)
fullLength = 0xc0 + len(data)
b = bytes([0x33, 0x35, 0x80 + len(data), *data,  0x80, fullLength])
print("-", b)
port.write(b)

# Receive bytes
nb = len(data)
print("Receiving at", brate)
print(nb, "bytes")
data = port.read(nb)
print('-', data)

#