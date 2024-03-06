import time
import serial

def getCurrentLocation():
	serial_port = '/dev/ttyUSB1'

	ser = serial.Serial(serial_port, baudrate=9600, timeout=10)

	longitude = 0
	latitude = 0

	try:
		line = ser.readline().decode('utf-8').strip()
		
		if line.startswith('$GPGGA'):
			data = line.split(',')
			#ser.close()
			return data

	except UnicodeDecodeError:
		print("UnicodeDecodeError: Unable to decode the received data.")
		

