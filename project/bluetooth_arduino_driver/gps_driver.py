#!/usr/bin/python3.7

import time
import dbus
import dbus.mainloop.glib
from gps_movement import gps_movement
from gi.repository import GLib



mainloop = None
gps = None

def gps_signal_received(waypoints):
    global gps
    print(waypoints[0], waypoints[1])
    

def main():
    global mainloop
    global gps

    gps = gps_movement()

    # Setup D-Bus main loop
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    print("In main")
    
    # Connect to the system bus
    bus = dbus.SystemBus()
    
    # Add a signal receiver for movement signals
    bus.add_signal_receiver(
        gps_signal_received,
        dbus_interface='tractorsquad.dummy.GPS',
        signal_name='GPSSignal'
    )

    # Start the GLib main loop to listen for signals
    mainloop = GLib.MainLoop()
    mainloop.run()

if __name__ == '__main__':
    main()
