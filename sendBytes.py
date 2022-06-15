# Enable pyserial extensions
import pyftdi.serialext
from bitstring import BitArray

brate = 230400

url = 'ftdi://ftdi:232:AQ00RVND/1'
# port = pyftdi.serialext.serial_for_url(url, baudrate=brate, bytesize=8, stopbits=1, parity='N', xonxoff=False, rtscts=False)


DAC_resolution = 2**12 -1 #4095

def voltageToBytesArray(voltage):
    voltageInDAC_resulution = int((voltage/2.5) * DAC_resolution)
    data = voltageInDAC_resulution.to_bytes(2, 'little')

    print(f'{voltage=}')
    print(f'{voltageInDAC_resulution=}')
    print(f'{data}\t\thex')

    bigEndianHex = hex(voltageInDAC_resulution)
    print(f'{bigEndianHex}\t\tbigEndianHex')
    num = voltageInDAC_resulution
    littleEndianBits = [(num >> shift_ind) & 1
             for shift_ind in range(num.bit_length())] # little endian
    bigEndianBits = list(reversed(littleEndianBits)) # big endian
    print(f'{littleEndianBits}\t\tlittleEndian')
    print(f'{bigEndianBits}\t\bigEndian')

    return bytes([0x80 + len(data), data[1], data[0], 0x80])

print("Transmition:")


voltage = 2.1
b = voltageToBytesArray(voltage)
print("-", b)
# port.write(b)

# # Receive bytes
# nb = len(data)
# print("receiving")
# print(nb, "bytes")
# #data = port.read(nb)
# print('-', data)

# #
