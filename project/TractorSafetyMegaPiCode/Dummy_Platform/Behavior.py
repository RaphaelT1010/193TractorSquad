from time import ctime, sleep
import GPS_Get_Heading as heading
import MotorHandler
import StraightLineMover as gps_position
import gps_modulo as gps
import DistanceCalculator	


def grabCoordinates():
	#print("Grabbing Current Coordinates")
	data = gps.getCurrentLocation()
	while(data is None):
		#print("Unable to retrieve GPS location.")
		data = gps.getCurrentLocation()
	#print(data)
	latitude = float(data[2][:2]) + float(data[2][2:]) / 60
	longitude = -(float(data[4][:3]) + float(data[4][3:]) / 60)
	#print("Latitude: {0:.6f} degrees".format(latitude))
	#print("Longitude: {0:.6f} degrees".format(longitude))
			
	#GPS function here to grab coordinates
	return [latitude, longitude]


def getAveragePosition():
	position = (0,0)
	n = 15	
	for i in range(n):
		print(f"Obtaining Coordinates #{i}")
		tempPosition = grabCoordinates()
		position = (position[0] + tempPosition[0], position[1] + tempPosition[1])
	position = (position[0]/n, position[1]/n)
	return position

def startUpProcedure(bot):
	print("-------------------------")
	print("Obtaining Inital position")
	print("-------------------------")
	initialPosition = getAveragePosition()
	print(f"initialPosition: {initialPosition}")
	
	# initialPosition = (38.536293, -121.753768)
	gps_position.moveStraight(initialPosition, bot)
	print("-------------------------")
	print("Obtaining Final position")
	print("-------------------------")
	finalPosition = getAveragePosition()
	print(f"finalPosition: {finalPosition}")

	#finalPosition = (38.536277, -121.753772)
	
	heading = DistanceCalculator.heading(initialPosition[0], initialPosition[1], finalPosition[0], finalPosition[1])

	return heading, finalPosition
	
	
	


