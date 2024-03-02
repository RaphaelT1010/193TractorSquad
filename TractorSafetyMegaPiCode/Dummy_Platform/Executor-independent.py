import Controller
from time import ctime,sleep
import threading
import keyboard
from pynput import keyboard
from functools import partial
import MotorHandler

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
