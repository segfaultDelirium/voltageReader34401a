#
# A.Skoczen, AGH0-UST
# 04.2021
# multimetr agilent 34401a -> RS-232 -> FTDI -> USB -> pyftdi
# przykład poprawnego rozwiązania pracy sygnałów DSR, DTR
#
import pyftdi.serialext
import time

brate = 9600
#url = "ftdi://ftdi:232:FT4T6R2Q/1"
# url = "ftdi://ftdi:232:FT4Q20IC/1"
url = 'ftdi://ftdi:232:FT4T6R2Q/1'
port = pyftdi.serialext.serial_for_url(url, baudrate=brate, timeout=10, bytesize=8, stopbits=2, parity='N')
#, xonxoff=False, rtscts=False, dsrdtr=True)

port.write(b'\x03')
#time.sleep(1)
print("DSR: ", port.dsr)
remote = "SYST:REM\n"
port.write(remote)
beep = "SYST:BEEP\n"
port.write(beep)
disp = "DISP:TEXT \"AGH WFiIS\"\n"
port.write(disp)
# Important !!!!!!
time.sleep(1)
id = "*IDN?\n"
print("DSR befor id:", port.dsr)
port.write(id)
print("DSR after id: ", port.dsr)
while port.dsr:
	pass
#	time.sleep(0.1)

print("DSR after loop: ", port.dsr)
# Important !!!!!!
port.dtr = True
data = port.read(1024)
port.dtr = False
print('-', data)

