import Controller
from time import ctime,sleep
import threading
import keyboard
from pynput import keyboard
from functools import partial
import MotorHandler
import GPS_Get_Heading as heading
import Behavior
import DistanceCalculator

def on_press(key,bot):
	try:
		# regular movements
		if key.char == "w":
			MotorHandler.driveBotForward(bot)
		if key.char =="a":
			MotorHandler.turnBotLeft(bot)
		if key.char == "d":
			MotorHandler.turnBotRight(bot)
		if key.char =="s":
			MotorHandler.driveBotInReverse(bot)
		if key.char =="q":
			MotorHandler.pivotBotLeft(bot)
		if key.char =="e":
			MotorHandler.pivotBotRight(bot)
		
		# preplanned movement
		if key.char == '1':
			print(f"numerical key {key.char} is pressed")
			MotorHandler.turn180Bot(bot)

		if key.char == '2':
			print(f"numerical key {key.char} is pressed")
			MotorHandler.turn360Bot(bot)

		if key.char == '3':
			print(f"numerical key {key.char} is pressed")
			MotorHandler.turn90Bot(bot)

		if key.char == '4':
			print("testing 4")
			heading.testheading(195, 45, bot= bot)

		if key.char == '5':
			print("testing 5")
			
			current_heading, last_pos = Behavior.startUpProcedure(bot)
			dest_heading = DistanceCalculator.heading(last_pos[0], last_pos[1], 38.536598333333345, -121.75459833333335)
			sleep(1)
			
			heading.faceCorrectHeading(dest_heading, current_heading, bot = bot)

		print('alphanumeric key{0} pressed'.format(key.char))
	except AttributeError:
		print('special key {0} pressed'.format(key))

def on_release(key,bot):
	print('{0} released'.format(key))
	MotorHandler.stopBot(bot)
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
