#!/usr/bin/python3.7

import sys

import dbus
import dbus.exceptions
import dbus.service
import dbus.mainloop.glib

from gi.repository import GLib
sys.path.insert(0, '.')

from exceptions import InvalidArgsException
from exceptions import NotSupportedException
from exceptions import NotPermittedException
from exceptions import InvalidValueLengthException
from exceptions import FailedException

import advertisement
from advertisement import Advertisement

import application
from application import Application

from service import Service
from service import Characteristic
from service import Descriptor

mainloop = None
adv = None
ad_manager = None
connected = 0
app = None
timeout = 0

DBUS_PROPERTIES = "org.freedesktop.DBus.Properties"

BLUEZ_SERVICE_NAME = 'org.bluez'
DEVICE_INTERFACE = 'org.bluez.Device1'
LE_ADVERTISING_MANAGER_IFACE = 'org.bluez.LEAdvertisingManager1'
GATT_MANAGER_IFACE = 'org.bluez.GattManager1'
DBUS_OM_IFACE = 'org.freedesktop.DBus.ObjectManager'
DBUS_PROP_IFACE = 'org.freedesktop.DBus.Properties'

class DummyAdvertisement(Advertisement):
    """
    Main Advertisement
    """
    def __init__(self, bus, index):
        Advertisement.__init__(self, bus, index, 'peripheral')
        self.add_service_uuid('0000ffe0-0000-1000-8000-00805f9b34fb')
        self.add_local_name('tractorsquad')
    
class DummyApplication(Application):
    """
    Main application
    """
    def __init__(self, bus):
        Application.__init__(self, bus)
        self.add_service(MovementService(bus, 0))
        self.add_service(GPSService(bus, 1))

class GPSService(Service):
    """
    Service that handles the GPS coordinate system
    """
    UUID = '0392fac1-9fd3-1023-a4e2-39109fa39aa2'

    def __init__(self, bus, index):
        Service.__init__(self, bus, index, self.UUID, True)
        self.add_characteristic(GPSChrc(bus, 0, self))
        self.waypoints = [0] * 256

    @dbus.service.signal('tractorsquad.dummy.GPS')
    def GPSSignal(self, value):
        pass

    def emitGPSSignal(self):
        print("sending GPS waypoints")
        self.GPSSignal(self.waypoints)
        print("success")

class GPSChrc(Characteristic):
    """
    Characteristic for GPS
    """
    UUID = '0102aaaa-3333-1111-abcd-0123456831fd'

    def __init__(self, bus, index, service):
        Characteristic.__init__(self, bus, index, self.UUID, ['write'], service)

    def WriteValue(self, value, option):
        print("Writing to GPS Chrc")
        received = dbus_to_python(value)

        index = (received[0] & 254) >> 1
        lon = ((received[0] & 1) << 28) + (received[1] << 20) + (received[2] << 12) + (received[3] << 4) + (received[4] >> 4)
        lat = ((received[4] & 15) << 24) + (received[5] << 16) + ((received[6] << 8) + received[7])

        if lon & (1 << 28) != 0: # if lon is negative
            lon |= -536870912
        if lat & (1 << 27) != 0: # if lat is negative
            lat |= -268435456

        print("Received: index =", index, "lon =", lon, "lat =", lat)

        self.service.waypoints[index * 2] = lon;
        self.service.waypoints[index * 2 + 1] = lat;

        self.service.emitGPSSignal();

class MovementService(Service):
    """
    Service that controls the basic movement
    """
    M_UUID = '0000ffe0-0000-1000-8000-00805f9b34fb'

    def __init__(self, bus, index):
        Service.__init__(self, bus, index, self.M_UUID, True)
        self.add_characteristic(MovementStateChrc(bus, 0, self))
        self.enabled = 0
        self.mstate = 0

    @dbus.service.signal('tractorsquad.dummy.Movement', signature='i')
    def MoveStateSignal(self, mstate):
        pass

    def emitMoveStateSignal(self):
        print("sending", self.mstate)
        self.MoveStateSignal(self.mstate)

class MovementStateChrc(Characteristic):
    """
    Characteristic that stores the movement state
    """
    M_STATE_UUID = '0000ffe1-0000-1000-8000-00805f9b34fb'

    def __init__(self, bus, index, service):
        Characteristic.__init__(self, bus, index, self.M_STATE_UUID, ['write'], service)

    def WriteValue(self, value, options):
        print("Writing to Movement State Chrc")

        received = int.from_bytes(dbus_to_python(value), "big")
        if received == 64:
            # acknowledgement
            print('Received', received)
            timeout = 0
        elif received == 38:
            # &, turn on
            print('Received', received, 'Turning on')
            self.service.enabled = 1
            self.service.mstate = 115
            timeout = 0
        elif received == 35:
            # #, turn off
            print('Received', received, 'Turning off')
            self.service.enabled = 0
            self.service.mstate = 115
        elif self.service.enabled:
            self.service.mstate = int.from_bytes(dbus_to_python(value), "big")
            print('ENABLED -> Move State updated to', self.service.mstate)
            timeout = 0
        else:
            print('Received', received, 'but not enabled')
            self.service.mstate = 115

        print('Move State updated to', self.service.mstate)
        
        print('Emitting move state signal')
        self.service.emitMoveStateSignal()

def set_connected_status(status):
    global connected
    if status == 0:
        print("disconnected")
        connected = 0
        start_advertising()
    else:
        print("connected")
        connected = 1
        stop_advertising()

def properties_changed(interface, changed, invalidated, path):
    if (interface == DEVICE_INTERFACE):
        if ("Connected" in changed):
            set_connected_status(changed["Connected"])

def interfaces_added(path, interfaces):
    if DEVICE_INTERFACE in interfaces:
        properties = interfaces[DEVICE_INTERFACE]
        if ("Connected" in properties):
            set_connected_status(properties["Connected"])

def register_ad_cb():
    print('Advertisement registered')

def register_ad_error_cb(error):
    print('Failed to register advertisement: ' + str(error))
    mainloop.quit()

def register_app_cb():
    print('GATT application registered')

def register_app_error_cb(error):
    print('Failed to register application: ' + str(error))
    mainloop.quit()

def start_advertising():
    global adv
    global ad_manager
    print("Registering Advertisement", adv.get_path())

    ad_manager.RegisterAdvertisement(adv.get_path(), {}, reply_handler=register_ad_cb, error_handler=register_ad_error_cb)

def stop_advertising():
    global adv
    global ad_manager
    print("Unregistering advertisement", adv.get_path())

    ad_manager.UnregisterAdvertisement(adv.get_path())

def dbus_to_python(data):
    if isinstance(data, dbus.String):
        data = str(data)
    if isinstance(data, dbus.ObjectPath):
        data = str(data)
    elif isinstance(data, dbus.Boolean):
        data = bool(data)
    elif isinstance(data, dbus.Int64):
        data = int(data)
    elif isinstance(data, dbus.Int32):
        data = int(data)
    elif isinstance(data, dbus.Int16):
        data = int(data)
    elif isinstance(data, dbus.UInt16):
        data = int(data)
    elif isinstance(data, dbus.Byte):
        data = int(data)
    elif isinstance(data, dbus.Double):
        data = float(data)
    elif isinstance(data, dbus.Array):
        data = [dbus_to_python(value) for value in data]
    elif isinstance(data, dbus.Dictionary):
        new_data = dict()
        for key in data.keys():
            new_data[key] = dbus_to_python(data[key])
        data = new_data
    return data

def check():
    global timeout
    global connected
    print("checker")
    if connected:
        #timeout += 1
        if timeout == 11:
            print("timeout")
            app.services[0].mstate = 115
            app.services[0].enabled = 0
    else:
        print("not connected")
        app.services[0].mstate = 115
        app.services[0].enabled = 0
    app.services[0].emitMoveStateSignal()
    return True

def main():
    global mainloop
    global adv
    global ad_manager
    global app

    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    bus = dbus.SystemBus()

    ad_adapter = advertisement.find_adapter(bus)

    if not ad_adapter:
        print('LEAdvertisingManager1 interface not found')
        return

    adapter_props = dbus.Interface(bus.get_object(BLUEZ_SERVICE_NAME, ad_adapter), "org.freedesktop.DBus.Properties")

    adapter_props.Set("org.bluez.Adapter1", "Powered", dbus.Boolean(1))

    ad_manager = dbus.Interface(bus.get_object(BLUEZ_SERVICE_NAME, ad_adapter), LE_ADVERTISING_MANAGER_IFACE)

    adv = DummyAdvertisement(bus, 0)

    bus.add_signal_receiver(properties_changed, dbus_interface = DBUS_PROPERTIES, signal_name = "PropertiesChanged", path_keyword = "path")

    bus.add_signal_receiver(interfaces_added, dbus_interface = DBUS_OM_IFACE, signal_name = "InterfacesAdded")

    start_advertising()

    adapter = application.find_adapter(bus)
    if not adapter:
        print('GattManager1 interace not found')
        return

    service_manager = dbus.Interface(bus.get_object(BLUEZ_SERVICE_NAME, adapter), GATT_MANAGER_IFACE)

    app = DummyApplication(bus)
    service_manager.RegisterApplication(app.get_path(), {}, reply_handler=register_app_cb, error_handler=register_app_error_cb)

#    timer = GLib.timeout_add(4500, check)

    mainloop = GLib.MainLoop()

    mainloop.run()


if __name__ == '__main__':
    main()
