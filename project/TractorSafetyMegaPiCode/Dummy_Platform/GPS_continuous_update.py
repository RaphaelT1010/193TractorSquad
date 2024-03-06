import time
import serial

import gps_modulo as gps

longitude = 0
latitude = 0

try:
	while True:
		#longitude, latitude = 
		data = gps.getCurrentLocation()
		while(data is None):
			print("Unable to retrieve GPS location.")
			data = gps.getCurrentLocation()
		print(data)
		latitude = float(data[2][:2]) + float(data[2][2:]) / 60
		longitude = -(float(data[4][:3]) + float(data[4][3:]) / 60)
		print("Latitude: {0:.6f} degrees".format(latitude))
		print("Longitude: {0:.6f} degrees".format(longitude))
		
		

except KeyboardInterrupt:
	exit()
