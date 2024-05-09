import MotorHandler


def faceCorrectHeading(destHeading, currentHeading, bot):
	print(f"currentHeading: {currentHeading}") 
	print(f"destHeading: {destHeading}") 
	resultheading = destHeading - currentHeading
	adj_heading = 360 - abs(resultheading)
	
	if adj_heading < 180:
		heading = adj_heading
		if resultheading < 0:
			MotorHandler.pivotCW(abs(heading), bot)
		else:
			MotorHandler.pivotCCW(abs(heading), bot)

	else: 
		heading = resultheading
		if resultheading < 0:
			MotorHandler.pivotCCW(abs(heading),bot)
		else:
			MotorHandler.pivotCW(abs(heading),bot)
