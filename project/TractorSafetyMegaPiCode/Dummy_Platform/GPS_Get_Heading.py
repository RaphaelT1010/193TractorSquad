import MotorHandler


def testheading(destHeading, currentHeading, bot):
	print("Inside of testHeading")
	resultheading = destHeading - currentHeading
	print(resultheading)
	if resultheading != 0:
		heading = 360 - abs(resultheading)
		if heading > 180:
			heading = resultheading

			
		if resultheading < 0:
			MotorHandler.pivotCCW(abs(heading), bot)
		else:
			MotorHandler.pivotCW(abs(heading), bot)
	else:
		print("heading is 0")

