import time
import serial

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
			print(data)
			#latitude = float(data[2])
			#longitude = float(data[4])
			latitude = float(data[2][:2]) + float(data[2][2:]) / 60
			longitude = -(float(data[4][:3]) + float(data[4][3:]) / 60)

			print("Latitude: {0:.6f} degrees".format(latitude))
			print("Longitude: {0:.6f} degrees".format(longitude))
			time.sleep(1)

except KeyboardInterrupt:
	ser.close()
