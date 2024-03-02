import Controller
from time import ctime,sleep
import threading
import keyboard
from pynput import keyboard
from functools import partial

## Start of Robot Controller functions
def printTheControlsPanel():
	print("Welcome to the Robot Controls!")
	print("To make the car move forward type: forward")
	print("To make the car move backwards type: reverse")
	print("To make the car turn left type: right")
	print("To make the car turn left type: left")
	print("To stop the car type: stop")

def driveBotForward(bot):
	bot.motorRun(1,50)
	bot.motorRun(2,-50)
	bot.motorRun(Controller.M1,50)
	bot.motorRun(Controller.M2,-50)


def driveBotInReverse(bot):
	bot.motorRun(1,-50)
	bot.motorRun(2,50)
	bot.motorRun(Controller.M1,-50)
	bot.motorRun(Controller.M2,50)

def turnBotRight(bot):
	bot.motorRun(1,-50)
	bot.motorRun(Controller.M1,-50)

def turnBotLeft(bot):
	bot.motorRun(1,50)
	bot.motorRun(Controller.M1,50)

def stopBot(bot):
	bot.motorRun(1,0)
	bot.motorRun(2,0)
	bot.motorRun(Controller.M1,0)
	bot.motorRun(Controller.M2,0)

# M1 = back right
# M2 = front left 
# 1 = front right 
# 2 = back left
