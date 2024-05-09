import time
import serial


serial_port = ''
ser = ''
longitude = 0
latitude = 0

def setupGPS():
	# open serial port 	
	serial_port = '/dev/ttyUSB0'
	ser = serial.Serial(serial_port, baudrate=9600, timeout=10)

	# initialize variables
	longitude = 0
	latitude = 0


def getGPSData():
	try:
		line = ser.readline().decode('utf-8').strip()
		
		if line.startswith('$GPGGA'):
			data = line.split(',')
			return data

	except UnicodeDecodeError:
		print("UnicodeDecodeError: Unable to decode the received data.")
		

def getLocation():
	setupGPS()		
	data = getGPSData()
	while(data is None):
		print("Unable to retrieve GPS location.")
		data = gps.getCurrentLocation()
	# print(data)

	latitude = float(data[2][:2]) + float(data[2][2:]) / 60
	longitude = -(float(data[4][:3]) + float(data[4][3:]) / 60)
	print("Latitude: {0:.6f} degrees".format(latitude))
	print("Longitude: {0:.6f} degrees".format(longitude))
			
			

		
