import time
import serial

class GPS_Robot:
	def __init__(self):
		print("Initializing GPS Module")
	
	def getCurrentLocation(self):
		serial_port = '/dev/ttyUSB1'

		ser = serial.Serial(serial_port, baudrate=9600, timeout=10)


		try:
			while True:
				try:
					line = ser.readline().decode('utf-8').strip()
				except UnicodeDecodeError:
					print("UnicodeDecodeError: Unable to decode the received data.")
					continue
				if line.startswith('$GPGGA'):
					data = line.split(',')
					latitude = float(data[2])
					longitude = float(data[4])
					print("Latitude: {0:.6f} degrees".format(latitude))
					print("Longitude: {0:.6f} degrees".format(longitude))
					time.sleep(1)

				if line.startswith('$GPHDT'):
					heading_data = line.split(',')
					heading = float(heading_data[1])
					print("Heading: {0:.2f} degrees".format(heading))
					time.sleep(1)

		except KeyboardInterrupt:
			ser.close()

