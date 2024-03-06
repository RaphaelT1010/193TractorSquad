from time import ctime, sleep
import GPS_Get_Heading as heading
import MotorHandler
import DistanceCalculator

#
def moveStraight(initialPosition, finalPosition, bot):

	# Calculate distance
	distance = DistanceCalculator.haversine(initialPosition[0], initialPosition[1], finalPosition[0], finalPosition[1])
	ratio = (1 / 14) #1 second per 14 cm
	completionTime = int(distance * ratio)
	print(f"StraightLineMover says distance is {distance}")
	print(f"StraightLineMover says time is {completionTime}")	

	MotorHandler.driveBotForward(bot)
	sleep(completionTime)

	MotorHandler.stopBot(bot)


def moveStraight(initialPosition, bot):

	# Calculate distance
	distance = 50 #cm
	ratio = (1 / 14) #1 second per 14 cm
	completionTime = int(distance * ratio)
	print(f"StraightLineMover says distance is {distance}")
	print(f"StraightLineMover says time is {completionTime}")	

	MotorHandler.driveBotForward(bot)
	sleep(completionTime)

	MotorHandler.stopBot(bot)
