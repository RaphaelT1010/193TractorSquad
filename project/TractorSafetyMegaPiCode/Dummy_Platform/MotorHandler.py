import Controller
from time import ctime,sleep
import threading
import keyboard
from pynput import keyboard
from functools import partial

## Start of Robot Controller functions
def printTheControlsPanel():
	print("Welcome to the Robot Controls!")
	print("----------------------------------------")
	print("User Controls")
	print("----------------------------------------")
	print("To make the car move forward type: w")
	print("To make the car move backwards type: s")
	print("To make the car turn left type: d")
	print("To make the car turn left type: a")
	print("To make the car pivot left type: q")
	print("To make the car pivot right type: e")
	print("To stop the car type: esc")
	print("----------------------------------------")
	print("Pre-programmed controls")
	print("----------------------------------------")
	print("1: Spin Bot 180 Degrees")
	print("2: Spin Bot 360 Degrees")
	print("3: Spin Bot 90 Degrees")
	print("4: Spin Bot to face correct dest heading")
	print("5: Have Robot Start to Point A to B")
	print("----------------------------------------")
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

def pivotBotRight(bot):
	bot.motorRun(1,-50)
	bot.motorRun(Controller.M1,-50)
	print("hello")
def pivotBotLeft(bot):
	bot.motorRun(1,50)
	bot.motorRun(Controller.M1,50)

def turnBotLeft(bot):
	bot.motorRun(1,50)
	bot.motorRun(Controller.M1,50)

def turnBotRight(bot):
	bot.motorRun(Controller.M2,-50)
	bot.motorRun(2,-50)


def stopBot(bot):
	bot.motorRun(1,0)
	bot.motorRun(2,0)
	bot.motorRun(Controller.M1,0)
	bot.motorRun(Controller.M2,0)

def turn180Bot(bot):
	pivotBotRight(bot)
	sleep(4.2)

def turn360Bot(bot):
	pivotBotRight(bot)
	sleep(8.4)

def turn90Bot(bot):
	pivotBotRight(bot)
	sleep(2.1)	

def pivotCCW(heading, bot):
	print(f"Turning counter clockwise by {heading} degrees")
	pivot_time = heading / 42.857
	print(pivot_time)
	pivotBotLeft(bot)
	sleep(pivot_time)

def pivotCW(heading, bot):
	print(f"Turning clockwise by {heading} degrees")
	pivot_time = heading / 42.857
	print(pivot_time)
	pivotBotRight(bot)
	sleep(pivot_time)


# M1 = back right
# M2 = front left 
# 1 = front right 
# 2 = back left
