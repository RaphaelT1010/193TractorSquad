import Controller
from time import ctime,sleep
import threading
import keyboard
from pynput import keyboard
from functools import partial
import MotorHandler
import InputHandler

if __name__ =='__main__':
	bot = Controller.MegaPi()
	bot.start()
	
	InputHandler.pingForMovement(bot)
