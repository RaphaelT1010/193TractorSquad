import Controller
from time import ctime,sleep
import threading
import keyboard
from pynput import keyboard
from functools import partial
import MotorHandler

def runGpsMode(bot):
	#run GPS algorithm that has a finite end
	#allow user/programmer to know that the algorithm has ended
	#or have user input to end the algorithm

def on_press(key,bot):
	try:
		if key.char == "w":
			MotorHandler.driveBotForward(bot)
		if key.char =="a":
			MotorHandler.turnBotLeft(bot)
		if key.char == "d":
			MotorHandler.turnBotRight(bot)
		if key.char =="s":
			MotorHandler.driveBotInReverse(bot)
		print('alphanumeric key{0} pressed'.format(key.char))
	except AttributeError:
		print('special key {0} pressed'.format(key))

def on_release(key,bot):
	print('{0} released'.format(key))
	MotorHandlerstopBot(bot)
	if key == keyboard.Key.esc:
	# Stop listener
		return False

def runManualMode(bot):
	# Collect events until released
	with keyboard.Listener(on_press=partial(on_press,bot= bot),on_release=partial(on_release, bot=bot)) as listener:
    		listener.join()

	# ...or, in a non-blocking fashion:
	listener = keyboard.Listener(
	    on_press=on_press,
	    on_release=on_release)
	listener.start()

def pingForMovement(bot):
	while true:
		print("Current modes:")
		print("1 - manual")
		print("2 - gps")
		mode = input("Please enter the movement mode: ")
		if mode == "gps":
			runGpsMode(bot)
			print("End of GPS mode")
			sleep(2)
		else if mode == "":
			runManualMode(bot)
			print("End of Manual mode")
			sleep(2)
		else if mode == "exit":
			print("End Bot Movement")
			break
		else:
			print("Error - Incorrect input")
