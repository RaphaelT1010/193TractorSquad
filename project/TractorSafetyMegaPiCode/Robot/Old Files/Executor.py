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


def on_press(key,bot):
	try:
		if key.char == "w":
			driveBotForward(bot)
		if key.char =="a":
			turnBotLeft(bot)
		if key.char == "d":
			turnBotRight(bot)
		if key.char =="s":
			driveBotInReverse(bot)
		print('alphanumeric key{0} pressed'.format(key.char))
	except AttributeError:
		print('special key {0} pressed'.format(key))
def on_release(key,bot):
	print('{0} released'.format(key))
	stopBot(bot)
	if key == keyboard.Key.esc:
	# Stop listener
		return False

# M1 = back right
# M2 = front left 
# 1 = front right 
# 2 = back left



if __name__ =='__main__':
	bot = Controller.MegaPi()
	bot.start()
	# Collect events until released
	with keyboard.Listener(on_press=partial(on_press,bot= bot),on_release=partial(on_release, bot=bot)) as listener:
    		listener.join()

# ...or, in a non-blocking fashion:
	listener = keyboard.Listener(
	    on_press=on_press,
	    on_release=on_release)
	listener.start()
