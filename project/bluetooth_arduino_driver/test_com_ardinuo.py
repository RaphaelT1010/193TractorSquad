import serial
import time

serial1 = serial.Serial('/dev/ttyACM0', 9600)

while True:
	serial1.write(b'0')
	time.sleep(1)
	serial1.write(b'9')
	time.sleep(1)


