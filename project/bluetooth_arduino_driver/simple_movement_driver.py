#!/usr/bin/python3.7

import serial
import time
import dbus
import dbus.mainloop.glib
from gi.repository import GLib
from motor import motor

mainloop = None
ser = None
m = None

def movement_signal_received(m_state):
    global m
    print(f"Signal received: {m_state}")

    if m_state == 117:
        print("Move forward signal received\n") 
        m.drive_forward()
    elif m_state == 108:
        print("Turn left signal received\n")
        m.turn_left()
    elif m_state == 114:
        print("Turn right signal received\n")
        m.turn_right()
    elif m_state == 100:
        print("Drive backwards signal received\n")
        m.drive_backwards()
    elif m_state == 115:
        print("Stop signal received\n")
        m.stop()
    elif m_state == 0:
        print("Stop and exit signal received\n")
        m.stop()
        mainloop.quit()
        return
    else:
        print("Unknown signal received, stopping\n")
        m.stop()
        return
    m.stop()

def main():
    global ser
    global m
    global mainloop
    
    # Initialize the serial connection (uncomment if needed)
    # ser = serial.Serial('/dev/ttyUSB1', 9600)
    time.sleep(2)
    
    # Initialize the motor
    m = motor()
    m.stop()
    
    # Setup D-Bus main loop
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    print("In main")
    
    # Connect to the system bus
    bus = dbus.SystemBus()
    
    # Add a signal receiver for movement signals
    bus.add_signal_receiver(
        movement_signal_received,
        dbus_interface='tractorsquad.dummy.Movement',
        signal_name='MoveStateSignal'
    )

    # Start the GLib main loop to listen for signals
    mainloop = GLib.MainLoop()
    mainloop.run()

if __name__ == '__main__':
    main()
