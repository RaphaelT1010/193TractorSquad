#!/usr/bin/python3.7

import serial
import time

from motor import motor

m = motor()
m.stop()
i = 0
for i in range(5):
	m.pivotCCW()    
m.stop()
